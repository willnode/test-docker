from flask import Flask, jsonify, render_template, request
import redis
import os
import socket

import requests_wrapper as requests

app = Flask(__name__)

# Connect to Valkey (Redis)
redis_host = os.getenv("VALKEY_HOST", "valkey")
redis_port = int(os.getenv("VALKEY_PORT", 6379))
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health_check():
    try:
        r.set("ping", "pong")
        redis_status = r.get("ping")
        return jsonify({"status": "ok", "redis": redis_status}), 200
    except Exception as e:
        return jsonify({"status": "error", "redis_error": str(e)}), 500

@app.route("/inet", methods=["GET"])
def fetch_inet():
    try:
        response = requests.get("https://api.ipify.org:443?format=json", timeout=3, family=socket.AF_INET)
        return jsonify(response.json()), 200
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/inet6", methods=["GET"])
def fetch_inet6():
    try:
        response = requests.get("https://api.ipify.org:443?format=json", timeout=3, family=socket.AF_INET6)
        return jsonify(response.json()), 200
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/headers", methods=["GET"])
def fetch_headers():
    return jsonify({k:v for k, v in request.headers.items()}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
