from flask import Flask, request
import threading
import queue
import requests
import json
import time

log_queue = queue.Queue()
alert_queue = queue.Queue()
app = Flask(__name__)

# Define services and any special rules
SERVICES = {
    'police': {"url": "http://police:5000/handle"},
    'ngo': {"url": "http://ngo:5000/handle", "skip_if": {"type": "Harassment"}},
    'legal': {"url": "http://legal:5000/handle"},
    'transport': {"url": "http://transport:5000/handle"}
}

def log_writer():
    while True:
        data = log_queue.get()
        print("[LOG]", json.dumps(data))

def should_skip_service(service_name, alert):
    service = SERVICES[service_name]
    skip_condition = service.get("skip_if", {})
    # Check if the service should be skipped based on the condition
    return all(alert.get(k) == v for k, v in skip_condition.items())

def distribute_alert(alert):
    for service_name, config in SERVICES.items():
        # Only skip the NGO service if the condition matches
        if service_name == "ngo" and should_skip_service(service_name, alert):
            print(f"[INFO] Skipping {service_name} for alert type: {alert.get('type')}")
            continue

        try:
            response = requests.post(config['url'], json=alert, timeout=5)
            if response.status_code != 200:
                print(f"[WARNING] {service_name} responded with status {response.status_code}")
        except Exception as e:
            print(f"[ERROR] Failed to send alert to {service_name}: {e}")

def distributor():
    while True:
        alert = alert_queue.get()
        distribute_alert(alert)

@app.route('/alert', methods=['POST'])
def receive_alert():
    alert = request.get_json()
    log_queue.put(alert)
    alert_queue.put(alert)
    return {"status": "received"}, 200

if __name__ == '__main__':
    threading.Thread(target=log_writer, daemon=True).start()
    threading.Thread(target=distributor, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
