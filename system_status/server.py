import json

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta, timezone
import uvicorn
import requests
import sys
from starlette.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime

app = FastAPI()

# allow all inputs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=['*'],
    allow_headers=['*']
)

#default value, could be overridden by a parameter passed in
PROMETHEUS_URL= "http://one.sce/prometheus"
#http://one.sce/prometheus
# Serve the static directory at the root
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
templates = Jinja2Templates(directory="templates")

#expects an optional parameter as the target URL
@app.get("/system_status/", response_class=HTMLResponse)
def page_generator(request: Request, target : str = "one.sce/prometheus"):

    global PROMETHEUS_URL

    # Get the current datetime
    local_datetime = datetime.now().astimezone()

    # Format the datetime object into a string, including the timezone offset
    # %Y: Year with century (e.g., 2025)
    # %m: Month as a zero-padded decimal number (e.g., 07)
    # %d: Day of the month as a zero-padded decimal number (e.g., 21)
    # %H: Hour (24-hour clock) as a zero-padded decimal number (e.g., 20)
    # %M: Minute as a zero-padded decimal number (e.g., 43)
    # %S: Second as a zero-padded decimal number (e.g., 55)
    # %z: UTC offset in the form +HHMM or -HHMM (e.g., -0700 for PDT)
    fetch_time = local_datetime.strftime("%Y-%m-%d %H:%M:%S") + " - Local Time Zone"

    #print(datetime_string)

    PROMETHEUS_URL = "http://" + target # override the URL if passed in a different value
    #print(PROMETHEUS_URL) #working
    current_data = default_access()
    range_data = range_access()
    return (templates.TemplateResponse
            ("my_template.html",
             {"request": request, "current_data": current_data,
                    "range_data": range_data, "fetch_time": fetch_time}))

@app.get("/current_status_raw")
# return to the client as JSON file
def default_access(query : str = "up" ):
    #print(PROMETHEUS_URL) #working
    """Sends a PromQL query to Prometheus and returns the results."""
    url = f"{PROMETHEUS_URL}/api/v1/query"
    params = {'query': query}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors
        print (response.json()['data']['result'])
        return response.json()['data']['result']
    except requests.exceptions.RequestException as e:
        print(f"Error querying Prometheus: {e}")
        return None


@app.get('/range_status_raw')
def range_access(query: str='min_over_time(up{job!=""}[1h])', step: int = 1):

    # Get current time in UTC (RFC3339 format)
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=23)

    # Format to RFC3339 (ISO 8601)
    now_str = now.isoformat()
    start_str = start.isoformat()
    """Sends a PromQL query to Prometheus and returns the results."""
    url = f"{PROMETHEUS_URL}/api/v1/query_range"
    params = {
        'query': query,
        'start': start_str,
        'end': now_str,
        'step': f'{step}h'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying Prometheus: {e}")
        return None

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=9100)
    print("service is running")
