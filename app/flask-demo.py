from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection via environment variable
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/flaskdb")
client = MongoClient(MONGO_URI)
db = client.get_default_database()
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
