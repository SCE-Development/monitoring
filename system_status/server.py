import json
import argparse
import os

from urllib.parse import urljoin
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta, timezone
import uvicorn
import requests
import sys
from starlette.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from zoneinfo import ZoneInfo

app = FastAPI()

# allow all inputs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=['*'],
    allow_headers=['*']
)

#default value, could be overridden by a parameter passed in
PROMETHEUS_URL= ""
#http://one.sce/prometheus
# Serve the static directory at the root
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
templates = Jinja2Templates(directory="templates")
now = datetime.now() # this variable will hold the datetime object at fetching time

def get_timestamps():
    global now
    start = now - timedelta(hours=23)

    # Format to UNIX timestamp
    now_str = int(now.timestamp())
    start_str = int(start.timestamp())
    end_str = now_str
    print([start_str, end_str])
    return [start_str, end_str]

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        default = "0.0.0.0",
        help = "provide the host in dotted decimal notation, default: 0.0.0.0"
    )
    parser.add_argument(
        "--port",
        default = 9100,
        help = "The port the sys-stat would be running, must be an int, default: 9100"
    )

    parser.add_argument(
        "--target",
        default = "http://one.sce/prometheus/",
        help = "The URL of the Prometheus metrics exporter, default: http://one.sce/prometheus"
    )

    return parser.parse_args()

#get the arguments
args = get_args()

#expects an optional parameter as the target URL
@app.get("/", response_class=HTMLResponse)
def page_generator(request: Request):
    target : str = args.target
    global PROMETHEUS_URL

    # Get the current datetime
    local_datetime = datetime.now(ZoneInfo("America/Los_Angeles"))

    # Format the datetime object into a string, including the timezone offset
    # %Y: Year with century (e.g., 2025)
    # %m: Month as a zero-padded decimal number (e.g., 07)
    # %d: Day of the month as a zero-padded decimal number (e.g., 21)
    # %H: Hour (24-hour clock) as a zero-padded decimal number (e.g., 20)
    # %M: Minute as a zero-padded decimal number (e.g., 43)
    # %S: Second as a zero-padded decimal number (e.g., 55)
    # %z: UTC offset in the form +HHMM or -HHMM (e.g., -0700 for PDT)
    fetch_time = local_datetime.strftime("%Y-%m-%d %H:%M:%S")

    #print(datetime_string)

    #PROMETHEUS_URL = "http://" + target # override the URL if passed in a different value
    #print(PROMETHEUS_URL) #working
    current_data = default_access()
    range_data = range_access()
    return (templates.TemplateResponse
            ("my_template.html",
             {"request": request, "current_data": current_data,
                    "range_data": range_data, "fetch_time": fetch_time}))

@app.get("/current_status_raw")
# return to the client as JSON file
def default_access():
    #print(PROMETHEUS_URL) #working
    """Sends a PromQL query to Prometheus and returns the results."""
    url = urljoin(args.target, "api/v1/query")
    print(f"url queried: {url}")
    params = {'query': "up"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors
        print (response.json()['data']['result'])
        return response.json()['data']['result'] # return as a dictionary
    except requests.exceptions.RequestException as e:
        print(f"Error querying Prometheus: {e}")
        return None


@app.get('/range_status_raw')
def range_access():
    global now
    now = datetime.now()
    query: str='min_over_time(up{job!=""}[1h])'
    step: int = 1
    [start_str, end_str] = get_timestamps()

    """Sends a PromQL query to Prometheus and returns the results."""
    #url = urljoin(args.target, "/prometheusapi/v1/query_range")
    url = urljoin(args.target, "api/v1/query_range")
    print(f"url queried: {url}")
    params = {
        'query': query,
        'start': start_str,
        'end': end_str,
        'step': f'{step}h'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json() # return as a dictionary
    except requests.exceptions.RequestException as e:
        print(f"Error querying Prometheus: {e}")
        return None

def range_access_parsed():
    #debugging
    from debug_data import special_input
    result = special_input["data"]["result"]
    #print(result) working
    #find out the start time string
    #1753161586
    #1753244386
    [start_str, end_str] = [1753161586, 1753244386]#get_timestamps()
    key_list = []
    for i in range(24):
        key_list.append(int(start_str) + i * 3600)
    print(key_list) # working

    string_list = []
    for element in result:
        status_str = ""
        key_list_counter = 0
        value_list_counter = 0
        value_list = element["values"]
        while (value_list_counter < len(value_list)): #since we have data for 24 hours
            if value_list[0] != key_list[key_list_counter]:
                # this means there's a missing metric from the value
                key_list_counter += 1
                status_str += "N" #insert an N representing no value
                continue

            if value[0] == key_list[key_list_counter]:
                if value[1] == "1":
                    status_str += "U" #append an U representing Up
                else:
                    status_str += "D" #append a D representing Down

            key_list_counter += 1
            value_list_counter += 1

        #after the for loop, status_str is now holding the status
        string_list.append({element["metric"]["instance"], status_str})

    print(string_list)

if __name__ == "__main__":
    #print("service is running")
    uvicorn.run("server:app", host=args.host, port=args.port, reload=True)
    #range_access_parsed()