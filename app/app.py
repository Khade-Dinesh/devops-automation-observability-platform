
from flask import Flask, jsonify, Response, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os
import socket
import datetime

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

@app.after_request
def record_request(response):
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.endpoint or "unknown",
        status=response.status_code
    ).inc()
    return response

@app.route("/")
def home():
    return jsonify({
        "message": "DevOps Monitoring Platform",
        "status": "running",
        "hostname": socket.gethostname(),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/info")
def info():
    return jsonify({
        "application": "DevOps Monitoring API",
        "version": "1.0",
        "environment": os.getenv("APP_ENV", "development"),
        "hostname": socket.gethostname()
    })

@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

