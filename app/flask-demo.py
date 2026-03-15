from flask import Flask, request, jsonify
from pymongo import MongoClient
from urllib.parse import quote_plus
import os

app = Flask(__name__)

# MongoDB connection built from individual env vars to handle special characters
MONGO_USER = os.environ.get("MONGO_USER", "flaskapp")
MONGO_PASS = os.environ.get("MONGO_PASS", "")
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost:27017")
MONGO_DB = os.environ.get("MONGO_DB", "flaskdb")

if MONGO_PASS:
    MONGO_URI = f"mongodb://{quote_plus(MONGO_USER)}:{quote_plus(MONGO_PASS)}@{MONGO_HOST}/{MONGO_DB}"
else:
    MONGO_URI = f"mongodb://{MONGO_HOST}/{MONGO_DB}"

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db["items"]


@app.route("/")
def health():
    return jsonify({"status": "ok", "message": "Flask app is running"})


@app.route("/data", methods=["GET"])
def get_data():
    try:
        items = list(collection.find({}, {"_id": 0}))
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/data", methods=["POST"])
def post_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        collection.insert_one(data)
        data.pop("_id", None)
        return jsonify({"message": "Item added", "item": data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
