from fastapi import FastAPI, HTTPException, Response
import uvicorn
import random
import prometheus_client as pc
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)
heads_count = pc.Counter(
    "heads_count",#metrics name
    "number of heads",#help text
)
tails_count = pc.Counter(
    "tails_count",#metrics name
    "number of tails",#help text
)
flip_count = pc.Counter(
    "flip_count",#metrics name
    "number of flips",#help text
)

# Counter for coin flips

@app.get("/")
def root():
    return({ "message": "hello world" })

@app.get("/flip")
def flip_coin(times = None):
    flip_counts = {
        "heads": 0,
        "tails": 0
    }

    if times is None:
        # Single flip when no parameter is provided
        # result = "heads" if random.random() > 0.5 else "tails"
        # flip_counts[result] += 1
        return flip_counts
    else:
        try:
            times_as_int = int(times)
            for i in range(times_as_int):
                result = "heads" if random.random() > 0.5 else "tails"
                flip_counts[result] += 1
            heads_count.inc(flip_counts["heads"])
            tails_count.inc(flip_counts["tails"])
            flip_count.inc(times_as_int)    
            return flip_counts
        except ValueError:
            return {"error": "Parameter 'times' must be a valid integer"}
        

@app.get("/metrics")
def get_metrics():
    return Response(
        media_type="text/plain",
        content = pc.generate_latest(),
    )
        


if __name__ == "__main__":
    uvicorn.run(app , host= "0.0.0.0", port=5000)

