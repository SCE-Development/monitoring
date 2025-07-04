from dataclasses import dataclass
from fastapi.responses import HTMLResponse
from prometheus_api_client import PrometheusConnect
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn 
from flags import get_args
import json
import time
import threading
import os
from datetime import datetime, timedelta
import pytz
import requests



app = FastAPI()

pacific_tz = pytz.timezone('US/Pacific')

templates = Jinja2Templates(directory="templates")

args = get_args()

prom = PrometheusConnect(url = args.promurl, disable_ssl=True)#this will query "http://prometheus:9090/api/v1/query?query=up"

metrics_data = []
up_hours = 24  

@dataclass
class metrics:
    job_name: str
    timestamp: float
    value: float

def check_status(query):
    params = {"query" : query}
    try:
        response = requests.get("http://prometheus:9090/api/v1/query", params = params)
        response.raise_for_status()# Raise an error for HTTP issues
        json_response = response.json()
        if json_response["status"]=="success":
            return True
        elif json_response["status"]==None:
            print("the status key does not exist!")
            return False
        else:
            return False

    except Exception as e:
        print(f"Error querying Prometheus: {e}")
        return None

def polling_loop(interval, config):
        while True: 
            global metrics_data
            metrics_data = []
            for hosts in config:
                service_name = hosts["job-id"]
                prom_query = hosts["query"]
                if prom_query == "up":  
                    process_up_query(prom_query, service_name)  
            time.sleep(interval)

service_data = {}

def process_up_query(query, service_name):
    global metrics_data, service_data
    process_time_query("time() - process_start_time_seconds", service_name)
    if not check_status(query="up"):
        print("status is not success, please look into it!!")
    try:
        result = prom.custom_query(query=query)
        if not result:
            print(f"No results for query: {query}")
            last_active = datetime.now(pacific_tz).strftime("%Y-%m-%d %H:%M:%S %Z")
            metrics_data.append({
                "instance": service_name,
                "status": "Error in querying"
            })
            return
        
        for metric in result:
            job_name = metric.get('metric',{}).get('job', "")#for later use in dataclass
            time_stamp = metric.get('value', [])[0]#for later use in dataclass
            value = metric.get('value', [])[1]
            # last_active = datetime.now(pacific_tz).strftime("%Y-%m-%d %H:%M:%S %Z")
            status = "Healthy" if float(value) > 0 else "Unhealthy"
            if status == "Unhealthy":
                current = get_first_match_time(prom=prom, prom_query="up", match_value=0, hours=up_hours)
                metrics_data.append({
                    "instance": service_name,
                    "status": current
                })
            else:
                metrics_data.append({
                    "instance": service_name,
                    "status": "Healthy"
                })
    except Exception as e:
        print(f"Error processing query '{query}': {e}")
        metrics_data.append({
            "instance": service_name,
            "status": "Unhealthy due to error!"
        })


def process_time_query(query, service_name):
    global metrics_data, up_hours
    try:
        result = prom.custom_query(query=query)
        if result and len(result) > 0:
            first_result = result[0]
            uptime_seconds = float(first_result["value"][1])
            up_hours = int(uptime_seconds/3600)
            if up_hours == 0:
                up_hours = 1
    except Exception as e:
        print(f"Error processing time query '{query}': {e}")

def get_first_match_time(prom, prom_query, match_value=0, hours=24):
    global metrics_data
    prom_query = "up"
    start_time = datetime.now() - timedelta(hours=hours)
    end_time = datetime.now() 

    try:
        result = prom.get_metric_range_data(
            metric_name=prom_query,
            start_time=start_time,
            end_time=end_time,
        )

        for series in result:
            saw_up = False
            for timestamp, value in reversed(series["values"]):
                v = float(value)
                if v == 1:
                    saw_up = True
                elif v == 0 and saw_up:
                    utc_time = datetime.utcfromtimestamp(float(timestamp))
                    pacific_time = utc_time.astimezone(pacific_tz)
                    readable_time = pacific_time.strftime("%Y-%m-%d %H:%M:%S %Z")
                    status = f"Unhealthy as of {readable_time}"
                    return status
    except Exception as e:
        print(f"Error in get_first_match_time: {e}")
        return "Error checking status history"


@app.get("/", response_class=HTMLResponse)
async def get_metrics(request: Request):
    return templates.TemplateResponse(
        "health.html", 
        {"request": request, "metrics": metrics_data, "timestamp": datetime.now(pacific_tz).strftime("%Y-%m-%d %H:%M:%S %Z")}
    )

def main():
    with open(args.json, "r") as file:
        config = json.load(file)

    polling_thread = threading.Thread(target = polling_loop, args = (args.interval,config), daemon=True)#The daemon=True ensures the thread exits when the main program exits.
    polling_thread.start()

    uvicorn.run(app, host="0.0.0.0", port=args.port)

if __name__ == "__main__":
    main()
