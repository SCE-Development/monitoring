import argparse
import datetime
import uvicorn
import requests
from dataclasses import dataclass
from typing import List
import time
from zoneinfo import ZoneInfo

from urllib.parse import urljoin
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


@dataclass
class TimestampAndValuePair:
    timestamp: str
    value: str

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "value": self.value
        }


@dataclass
class PrometheusData:
    instance: str
    job: str
    hasData: bool
    is_up: bool
    values: List[TimestampAndValuePair]

    def to_dict(self):
        return {
            "instance": self.instance,
            "job": self.job,
            "hasData": self.hasData,
            "is_up": self.is_up,
            "values": [v.to_dict() for v in self.values]
        }

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# http://one.sce/prometheus, Serve the static directory at the root
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
templates = Jinja2Templates(directory="templates")


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="provide the host in dotted decimal notation, default: 0.0.0.0",
    )
    parser.add_argument(
        "--port",
        default=9100,
        help="The port the sys-stat would be running, must be an int, default: 9100",
    )

    parser.add_argument(
        "--target",
        default="http://one.sce/prometheus/",
        help="The URL of the Prometheus metrics exporter, default: http://one.sce/prometheus",
    )

    return parser.parse_args()


args = get_args()

def check_epoch_aggreement(epoch_time: int, assumed_epoch: int) -> bool:
    #Ensures the epoch times from the data set are within the expected range, using the global scrape intervval for reference
    aggreement = abs(epoch_time - assumed_epoch) < 5
    return aggreement


def get_prometheus_data() -> list[PrometheusData]:
    """Sends a PromQL query to Prometheus and returns the results."""
    """
    the response json looks like:
    {
        "status": "success",
        "data": {
            "resultType": "matrix",
            "result": [
                {
                    "metric": {
                        "instance": "192.168.69.141:8000",
                        "job": "SCE-tv-pi"
                    },
                    "values": [
                        [1753591741, "1"],
                        [1753595341, "1"]
                    ]
                }
            ]
        }
    }
    """
    url = urljoin(args.target, "api/v1/query_range")
    now = datetime.datetime.now()
    params = {
        "query": 'min_over_time(up{job!=""}[1h])',
        "start": int((now - datetime.timedelta(hours=23)).timestamp()),
        "end": int(now.timestamp()),
        "step": "1h",
    }
    result = []
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_json = response.json()
        result_list = response_json.get("data", {}).get("result", [])

        for service_dict in result_list:
            maybe_instance = service_dict.get("metric", {}).get(
                "instance", "NO INSTANCE AVAILABLE"
            )
            maybe_job = service_dict.get("metric", {}).get("job", "NO JOB AVAILABLE")
            maybe_values = service_dict.get("values", [])

    
            timestamps_and_values = []
            
            expected_epochs = []
            # generate the expected epoch times based on start time and 1 hour intervals
            current_epoch = int(params.get("start"))
            for _ in range(24):
                expected_epochs.append(current_epoch)
                current_epoch += 3600
            for epoch_value in expected_epochs:
                #catch for if the maybe_values queue is empty
                if not maybe_values:
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(epoch_value))
                    timestamps_and_values.append(TimestampAndValuePair(timestamp, "-1")) #-1 for no data
                    continue

                actual_epoch = maybe_values[0][0]
                if not check_epoch_aggreement(int(actual_epoch), epoch_value):
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(epoch_value))
                    timestamps_and_values.append(TimestampAndValuePair(timestamp, "-1")) #-1 for no data
                else:
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(actual_epoch))
                    timestamps_and_values.append(TimestampAndValuePair(timestamp, maybe_values[0][1]))
                    maybe_values.pop(0)
   
            # the service is up if the maximum timestamp's value is "1"
            # prometheus returns data with the greatest timestamp last
            is_up = False
            hasData = False
            if timestamps_and_values:
                if timestamps_and_values[-1].value == "-1":
                    is_up = False
                    hasData = False
                else:
                    hasData = True
                    is_up = timestamps_and_values[-1].value == "1"
                    
                
            service = PrometheusData(
                maybe_instance, maybe_job, hasData, is_up, timestamps_and_values
            )
            result.append(service)

        return result
    except requests.exceptions.RequestException as e:

        return []


# expects an optional parameter as the target URL
@app.get("/", response_class=HTMLResponse)
def page_generator(request: Request):
    local_datetime = datetime.datetime.now(ZoneInfo("America/Los_Angeles"))

    fetch_time = local_datetime.strftime("%Y-%m-%d %H:%M:%S")
    data = get_prometheus_data()
    if "json" in request.query_params:
        return JSONResponse(content=[d.to_dict() for d in data])

    return templates.TemplateResponse(
        "my_template.html", {"request": request, "data": data, "fetch_time": fetch_time}
    )


@app.get("/hello")
def hello():
    return "hello!"


if __name__ == "__main__":
    uvicorn.run("server:app", host=args.host, port=args.port, reload=True)
