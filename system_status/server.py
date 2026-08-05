import argparse
import datetime
import uvicorn
import requests
from dataclasses import dataclass
from typing import List, Optional
from zoneinfo import ZoneInfo

from urllib.parse import urljoin
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


DISPLAY_TIMEZONE = ZoneInfo("America/Los_Angeles")
HISTORY_POINT_COUNT = 24
HISTORY_STEP_SECONDS = 60 * 60
HISTORY_TIMESTAMP_TOLERANCE_SECONDS = 5


@dataclass
class TimestampAndValuePair:
    timestamp: str
    value: Optional[str]

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "value": self.value
        }


@dataclass
class PrometheusData:
    instance: str
    job: str
    has_data: bool
    is_up: bool
    values: List[TimestampAndValuePair]

    def to_dict(self):
        return {
            "instance": self.instance,
            "job": self.job,
            "has_data": self.has_data,
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


def build_history_values(
    prometheus_values: list, start_epoch: int
) -> List[TimestampAndValuePair]:
    """Return 24 fixed hourly slots, using None when Prometheus has no sample."""
    values_by_slot = {}
    for epoch_time, value in prometheus_values:
        epoch_time = float(epoch_time)
        slot = round((epoch_time - start_epoch) / HISTORY_STEP_SECONDS)
        expected_epoch = start_epoch + slot * HISTORY_STEP_SECONDS
        if (
            0 <= slot < HISTORY_POINT_COUNT
            and abs(epoch_time - expected_epoch)
            <= HISTORY_TIMESTAMP_TOLERANCE_SECONDS
        ):
            values_by_slot[slot] = value

    history_values = []
    for slot in range(HISTORY_POINT_COUNT):
        epoch_time = start_epoch + slot * HISTORY_STEP_SECONDS
        local_timestamp = datetime.datetime.fromtimestamp(
            epoch_time, DISPLAY_TIMEZONE
        )
        timestamp = local_timestamp.strftime("%Y-%m-%d | %H:%M:%S %Z")
        history_values.append(
            TimestampAndValuePair(timestamp, values_by_slot.get(slot))
        )

    return history_values


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
        "start": int(
            (now - datetime.timedelta(hours=HISTORY_POINT_COUNT - 1)).timestamp()
        ),
        "end": int(now.timestamp()),
        "step": str(HISTORY_STEP_SECONDS),
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

            timestamps_and_values = build_history_values(
                maybe_values, params["start"]
            )

            # the service is up if the maximum timestamp's value is "1"
            # prometheus returns data with the greatest timestamp last
            latest_value = timestamps_and_values[-1].value
            has_data = latest_value is not None
            is_up = latest_value == "1"
            service = PrometheusData(
                maybe_instance,
                maybe_job,
                has_data,
                is_up,
                timestamps_and_values,
            )
            result.append(service)

        return result
    except requests.exceptions.RequestException as e:

        return []


# expects an optional parameter as the target URL
@app.get("/", response_class=HTMLResponse)
def page_generator(request: Request):
    local_datetime = datetime.datetime.now(DISPLAY_TIMEZONE)

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
