from prometheus_client import Counter, Histogram

prefix = "tracardi"

REQUEST_COUNT = Counter(
    f"{prefix}_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)

REQUEST_LATENCY = Histogram(
    f"{prefix}_request_duration_seconds",
    "HTTP request latency",
    ["endpoint"],
)

QUEUE_PHASE_LATENCY = Histogram(
    f"{prefix}_queue_duration_seconds",
    "Data to queue latency",
    ["phase"],
)