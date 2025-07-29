import argparse
import uvicorn
import requests

from urllib.parse import urljoin

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from datetime import datetime, timedelta
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
    # %Y: Year # %m: Month as int  # %d: Day of month as int # %H: Hour as int
    # %M: Minute as int # %S: Second as int
    fetch_time = local_datetime.strftime("%Y-%m-%d %H:%M:%S")

    #print(datetime_string)

    #PROMETHEUS_URL = "http://" + target # override the URL if passed in a different value
    #print(PROMETHEUS_URL) #working
    current_data = default_access_parsed() # a dict
    range_data = range_access_parsed() # a list
    key_list = current_data.keys()
    for i in range(len(current_data)):
        if (current_data[f"service_{i}"]["detail"] == range_data[i]["detail"]):
            current_data[f"service_{i}"]["range_status"] =  range_data[i]["status"]
            current_data[f"service_{i}"]["warning"] =  range_data[i]["warning"]
    print(current_data)

    return (templates.TemplateResponse
            ("my_template.html",
             {"request": request, "data": current_data, "fetch_time": fetch_time}))

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

def default_access_parsed():
    #debugging
    #import debug_data
    #default_list = debug_data.non_input
    default_list = default_access()
    parse_dict = {}
    if not default_list:
        return {"service_0": {"job": "no job found", "detail": "-", "current_status": "-"}}

    for i in range(len(default_list)):
        parse_dict[f"service_{i}"] = {
            "job": default_list[i]["metric"]["job"],
            "detail": default_list[i]["metric"]["instance"],
            "current_status": default_list[i]["value"][1]
        }
    print(default_list)
    print(parse_dict)
    return parse_dict


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
    #import debug_data
    #result = debug_data.special_input
    #result = debug_data.non_input
    result = range_access()
    if not result: # if the result is a falsy value
        return[{"detail": "-", "status": "-"}]

    #only do the rest if the input is not None
    #result = debug_data.non_input["data"]["result"]
    #result = debug_data.special_input["data"]["result"]
    result = range_access()["data"]["result"]
    #print(result) #working
    #find out the start time string
    #1753161586
    #1753244386
    [start_str, end_str] = get_timestamps()#[1753161586, 1753244386]#
    key_list = []
    for i in range(24):
        key_list.append(int(start_str) + i * 3600)

    #print(key_list) # working
    if end_str == key_list[-1]:
        print("working") #check if the last key matches the end key of the actual data

    status_str_list = []
    for element in result:
        #continue
        status_str = ""
        key_list_counter = 0
        value_list_counter = 0
        value_list = element["values"]
        while (value_list_counter < len(value_list)): #since we have data for 24 hours
            if value_list[value_list_counter][0] != key_list[key_list_counter]:
                # this means there's a missing metric from the value
                key_list_counter += 1
                status_str += "N" #insert an N representing no value
                continue

            if value_list[value_list_counter][0] == key_list[key_list_counter]:
                if value_list[value_list_counter][1] == "1":
                    status_str += "U" #append an U representing Up
                else:
                    status_str += "D" #append a D representing Down

            key_list_counter += 1
            value_list_counter += 1

        #calculate the down and null time

        warning_list = {"down": [], "null": []}
        down_count = 0
        null_count = 0
        previous_status = "U"
        char_index = 0

        for char in status_str:
            if char == "U": previous_status = "U" #if everything is normal
            elif char == "D" and previous_status != "D": #new down occurrence
                previous_status = "D" #update the previous status
                warning_list["down"].append([key_list[char_index]-3600, key_list[char_index]]) #log the start and end of that entry
                down_count += 1
            elif char == "D" and previous_status == "D": #continuous down
                # no need to update the previous status
                warning_list["down"][down_count-1][1] = key_list[char_index] #update the end of the last entry
                #no need to update down count cuz it's continuous
            elif char == "N" and previous_status != "N": #new null occurrence
                previous_status = "N" #update the previous status
                warning_list["null"].append([key_list[char_index]-3600, key_list[char_index]]) #log the start and end of that entry
                null_count += 1
            elif char == "N" and previous_status == "N": #continuous null
                # no need to update the previous status
                warning_list["null"][down_count-1][1] = key_list[char_index] #update the end of the last entry
                #no need to update down count cuz it's continuous
            char_index += 1
        #print("down: ", down_count, "| ", "null :", null_count, "| ", warning_list)

        #convert the warning_list into warning string to send to the template
        pacific_tz = ZoneInfo("America/Los_Angeles")
        warning_str = ""
        down_str = ""
        null_str = ""
        if warning_list["down"]: #if there's any down
            down_str += "Down between:"
            for down in warning_list["down"]:
                down_str += "<br>" # the forbidden html injection hehe
                #start = int(down[0])
                #end = int(down[1])
                start = datetime.fromtimestamp(int(down[0]), pacific_tz)
                start_time = start.strftime("%m-%d %H:%M")
                end = datetime.fromtimestamp(int(down[1]), pacific_tz)
                end_time = end.strftime("%m-%d %H:%M")
                down_str += f" ⚡ {start_time} - {end_time}"
        if warning_list["null"]: # if there's any null data
            null_str += "No data between:"
            for null in warning_list["null"]:
                null_str += "<br>" # the forbidden html injection hehe
                #start = int(down[0])
                #end = int(down[1])
                start = datetime.fromtimestamp(int(null[0]), pacific_tz)
                start_time = start.strftime("%m-%d %H:%M")
                end = datetime.fromtimestamp(int(null[1]), pacific_tz)
                end_time = end.strftime("%m-%d %H:%M")
                null_str += f" ⚡ {start_time} - {end_time}"

        #combine the two strings
        if down_str:
            warning_str = f"{down_str}<br>{null_str}"
        else:
            warning_str = f"{null_str}"
        #after the for loop, status_str is now holding the status
        #print(warning_str)
        status_str_list.append({"detail": element["metric"]["instance"], "status":status_str, "warning": warning_str})




    #print(status_str_list)
    return status_str_list

if __name__ == "__main__":
    #print("service is running")
    uvicorn.run("server:app", host=args.host, port=args.port, reload=True)
    #range_access_parsed()
    #default_access_parsed()
    #page_generator()