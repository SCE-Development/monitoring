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
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


@dataclass
class TimestampAndValuePair:
    timestamp: datetime.datetime
    value: str


@dataclass
class PrometheusData:
    instance: str
    job: str
    is_up: bool
    values: List[TimestampAndValuePair]


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


def get_prometheus_data():# -> list[PrometheusData]:
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
                        "job": "sce-tv-pi"
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
        "start": str((now - datetime.timedelta(hours=23)).timestamp()),
        "end": str(now.timestamp()),
        "step": "1h",
    }
    result = []
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_json = response.json()
        result_list = response_json["data"]["result"]

        for service_dict in result_list:
            maybe_instance = service_dict.get("metric", {}).get(
                "instance", "NO INSTANCE AVAILABLE"
            )
            maybe_job = service_dict.get("metric", {}).get("job", "NO JOB AVAILABLE")
            maybe_values = service_dict.get("values", [])

            timestamps_and_values = []
            for epoch_time, value in maybe_values:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(epoch_time))
                timestamps_and_values.append(TimestampAndValuePair(timestamp, value))

            # the service is up if the maximum timestamp's value is "1"
            # prometheus returns data with the greatest timestamp last
            is_up = False
            if timestamps_and_values:
                is_up = timestamps_and_values[-1].value == "1"
            service = PrometheusData(
                maybe_instance, maybe_job, is_up, timestamps_and_values
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

    return templates.TemplateResponse(
        "my_template.html", {"request": request, "data": data, "fetch_time": fetch_time}
    )


@app.get("/hello")
def hello():
    return "hello!"


if __name__ == "__main__":
    uvicorn.run("server:app", host=args.host, port=args.port, reload=True)
