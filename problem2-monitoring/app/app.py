import random
import time

from prometheus_client import Counter, Gauge, Histogram, start_http_server

REQUESTS = Counter("app_requests_total", "Total requests", ["status"])
LATENCY = Histogram(
    "app_request_latency_seconds",
    "Request latency in seconds",
    buckets=[0.05, 0.1, 0.25, 0.5, 1, 2, 5],
)
QUEUE = Gauge("app_queue_depth", "Jobs waiting in the queue")


def error_rate():
    # Minute 4 of every 5-minute cycle simulates an incident.
    minute = int(time.time() // 60) % 5
    return 0.30 if minute == 4 else 0.02


def main():
    start_http_server(8000)
    print("Metrics available on port 8000", flush=True)
    while True:
        latency = random.uniform(0.03, 0.3)
        if random.random() < 0.05:
            latency += random.uniform(0.5, 2.0)  # occasional slow request
        LATENCY.observe(latency)
        status = "500" if random.random() < error_rate() else "200"
        REQUESTS.labels(status=status).inc()
        QUEUE.set(random.randint(0, 20))
        time.sleep(0.2)


if __name__ == "__main__":
    main()