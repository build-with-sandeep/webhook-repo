from flask import Blueprint, request, jsonify
from datetime import datetime
from app.extensions import mongo
from flask_cors import cross_origin

webhook = Blueprint('webhook', __name__, url_prefix='/webhook')

@webhook.route('/', methods=["GET"])
def root():
    print("hello world")
    return 'cool',200


@webhook.route('/receiver/', methods=["POST"])
@cross_origin()
def receiver():
    print("cool")
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json
    print(payload)

    if event_type not in ["push", "pull_request" , "merge"]:
        return jsonify({"status": "ignored"}), 200

    event_data = {
        "request_id" : "",
        "action": event_type,
        "timestamp": datetime.utcnow(),
        "author": payload["sender"]["login"],
        "to_branch": "",
        "from_branch": "",
    }

    if event_type == "push":
        event_data["request_id"]= payload["commits"][0]["id"]
        ref = payload["ref"]
        event_data["to_branch"] = ref.split("/")[-1]

    elif event_type == "pull_request" and payload["action"] in ["opened"] :
        event_data["request_id"] = payload["pull_request"]["id"]
        event_data["from_branch"] = payload["pull_request"]["head"]["ref"]
        event_data["to_branch"] = payload["pull_request"]["head"]["ref"]

    mongo.db.events.insert_one(event_data)
    print("hello---------")
    return jsonify({"status": "success"}), 200


@webhook.route('/events/', methods=["GET"])
@cross_origin()
def get_events():
    print("hello")
    try:
        events = list(mongo.db.events.find(
            {},
            {'_id': 0}
        ).sort("timestamp", -1))

        # Convert timestamps to string format
        for event in events:
            event["timestamp"] = event["timestamp"].strftime("%d %B %Y - %I:%M %p UTC")

        return jsonify(events), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500