"""
Flask Application for Kubernetes Demo
Features:
- Visit tracking with session management
- Pod identification for cluster debugging
- Request inspection for troubleshooting
- Designed for high availability deployment
"""

from flask import Flask, session, request
import socket

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

visitor_count = 0  # Global counter for unique visitors

@app.route('/')
def index():
    """
    Root endpoint that tracks unique visitors using session cookies.
    Increments counter only for first-time visitors.
    """
    global visitor_count
    if 'visited' not in session:
        session['visited'] = True
        visitor_count += 1
    return f"Visitor count: {visitor_count}"

@app.route("/hostname")
def get_hostname():
    """
    Returns the pod hostname for Kubernetes deployment verification.
    Useful for testing load balancing and pod distribution.
    """
    hostname = socket.gethostname()
    return f"Hostname :: {hostname}"

@app.route("/request-url")
def request_url():
    """
    Debugging endpoint that returns the full request URL.
    Helps verify ingress routing and request handling.
    """
    return f"Request URL: {request.url}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Listen on all interfaces for container networking