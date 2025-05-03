"""
K8s Demo App
Features:
- Visit tracking
- Pod identity
- Request info
"""

from flask import Flask, session, request
import socket

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Session store

visitor_count = 0  # Visit tracker

@app.route('/')
def index():
    """Count unique visits."""
    global visitor_count
    if 'visited' not in session:
        session['visited'] = True
        visitor_count += 1
    return f"Visitor count: {visitor_count}"

@app.route("/hostname")
def get_hostname():
    """Pod identifier."""
    hostname = socket.gethostname()
    return f"Hostname :: {hostname}"

@app.route("/request-url")
def request_url():
    """Debug endpoint."""
    return f"Request URL: {request.url}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Network access