import sys
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

ANALYTICS_URL = "http://analytics:5000/analyze"

def forward_to_analytics(data):
    try:
        response = requests.post(ANALYTICS_URL, json=data, timeout=5)
        print("[TRANSPORT] Forwarded to analytics, got:", response.json())
        return response.json(), 200
    except requests.exceptions.RequestException as e:
        print("[TRANSPORT] Failed to forward to analytics:", e)
        return {"error": "Failed to forward to analytics"}, 500

@app.route('/handle', methods=['POST'])
def handle_transport():
    data = request.get_json()
    print("[TRANSPORT] Received:", data)
    sys.stdout.flush()

    response_data, status = forward_to_analytics(data)
    sys.stdout.flush()
    return jsonify(response_data), status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
