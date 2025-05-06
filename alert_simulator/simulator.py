import sys
from flask import Flask, request

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    print("[ANALYTICS] Data received for analysis:", data)
    sys.stdout.flush()

    # Simulate some analysis logic
    result = {
        "status": "analyzed",
        "summary": f"Incident type: {data.get('type')} at {data.get('location')}"
    }

    return result, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
