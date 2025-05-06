import sys
from flask import Flask, request

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    print("[ANALYTICS] Data received for analysis:", data)
    sys.stdout.flush()  # flush output immediately
    return {"status": "analytics processed"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
