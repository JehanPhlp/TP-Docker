# app.py
import os
from flask import Flask, jsonify
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)

# --- MongoDB setup (minimal) ---
# Read the MongoDB URI from env; works with both mongodb:// and mongodb+srv://
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "testdb")

# Create a single, reusable client (connection pooling is built-in)
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)  # short timeout
db = client[MONGO_DB_NAME]


@app.route("/")
def hello():
    return "Hello, World! Depuis Flask dans Docker 🚀"


@app.route("/mongo/ping")
def mongo_ping():
    """
    Minimal health check to verify MongoDB connectivity.
    """
    try:
        # ping the server (doesn't require auth on its own; will fail if unreachable)
        client.admin.command("ping")
        return jsonify(status="ok", db=MONGO_DB_NAME), 200
    except PyMongoError as e:
        return jsonify(status="error", error=str(e)), 500


@app.route("/mongo/demo")
def mongo_demo():
    """
    Tiny demo: upsert a counter in 'counters' collection and return the value.
    Safe and idempotent for testing.
    """
    try:
        doc = db.counters.find_one_and_update(
            {"_id": "visits"},
            {"$inc": {"value": 1}},
            upsert=True,
            return_document=True,
        )
        return jsonify(counter=doc.get("value", 1)), 200
    except PyMongoError as e:
        return jsonify(status="error", error=str(e)), 500


if __name__ == "__main__":
    # Flask listens on all interfaces inside Docker
    app.run(host="0.0.0.0", port=5000)


