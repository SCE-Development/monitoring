from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta, timezone
import uvicorn
import requests
import sys
from starlette.staticfiles import StaticFiles

app = FastAPI()

# allow all inputs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=['*'],
    allow_headers=['*']
)

PROMETHEUS_URL= "http://one.sce/prometheus"

# Serve the static directory at the root
app.mount("/system_status", StaticFiles(directory="static", html=True), name="index")


@app.get("/current_status_raw")
# return to the client as JSON file
def default_access(query : str = "up" ):

    """Sends a PromQL query to Prometheus and returns the results."""
    url = f"{PROMETHEUS_URL}/api/v1/query"
    params = {'query': query}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()['data']['result']
    except requests.exceptions.RequestException as e:
        print(f"Error querying Prometheus: {e}")
        return None


@app.get('/range_status_raw')
def range_access(query: str='up', step: int = 1):

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
        return response.json()#['data']['result']
    except requests.exceptions.RequestException as e:
        print(f"Error querying Prometheus: {e}")
        return None




# Save original stdout
o = sys.stdout

# Redirect stdout to a file
with open('output.txt', 'w') as f:
    sys.stdout = f

    def query_prometheus(query):
        """Sends a PromQL query to Prometheus and returns the results."""
        url = f"{PROMETHEUS_URL}/api/v1/query"
        params = {'query': query}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status() # Raise an exception for HTTP errors
            return response.json()['data']['result']
        except requests.exceptions.RequestException as e:
            print(f"Error querying Prometheus: {e}")
            return None

    # Example usage: Get the current value of a metric
    query = 'up' # Example PromQL query
    results = query_prometheus(query)

    if results:
        for result in results:
            print(f"Metric: {result['metric']}, Value: {result['value'][1]}")

# Restore stdout
sys.stdout = o

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=9100)
