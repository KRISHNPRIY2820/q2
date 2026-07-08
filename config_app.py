from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

base_config = {
    "port": 8824,
    "workers": 6,
    "debug": False,
    "log_level": "warning",
    "api_key": "key-7etvzhzi1i",
}


def convert(key, value):
    if key in ("port", "workers"):
        return int(value)

    if key == "debug":
        return value.lower() in ("true", "1", "yes", "on")

    return str(value)


@app.get("/effective-config")
def effective_config(set: list[str] = Query(default=[])):
    cfg = base_config.copy()

    for item in set:
        if "=" not in item:
            continue

        k, v = item.split("=", 1)
        cfg[k] = convert(k, v)

    cfg["api_key"] = "****"

    return cfg
