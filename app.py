from flask import Flask, jsonify, render_template
import redis
import requests
import os

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

@app.route("/external", methods=["GET"])
def fetch_external():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=3)
        return jsonify(response.json()), 200
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
