from prometheus_client import Counter, Histogram

# Define Prometheus metrics

# Counter for counting requests
REQUESTS = Counter("requests_total", "Total number of requests", ["endpoint"])

# Counter for counting errors
ERRORS = Counter("errors_total", "Total number of errors", ["endpoint", "error_type"])

# Histogram for measuring request duration
REQUEST_DURATION = Histogram(
    'request_duration_seconds',
    'Duration of requests in seconds',
    ['endpoint']
)