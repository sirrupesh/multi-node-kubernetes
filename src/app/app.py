"""
Simple Flask Application for Kubernetes Demo
Provides basic endpoints for visitor counting, hostname display, and request URL information.
"""

from flask import Flask, session, request
import socket

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management

# Global counter for visitors
visitor_count = 0

@app.route('/')
def index():
    """Track and display visitor count using session data."""
    global visitor_count
    if 'visited' not in session:
        session['visited'] = True
        visitor_count += 1
    return f"Visitor count: {visitor_count}"

@app.route("/hostname")
def get_hostname():
    """Return the container hostname for Kubernetes pod identification."""
    hostname = socket.gethostname()
    return f"Hostname :: {hostname}"

@app.route("/request-url")
def request_url():
    """Display the current request URL for debugging and demo purposes."""
    return f"Request URL: {request.url}"

if __name__ == "__main__":
    # Run the application on all interfaces
    app.run(host="0.0.0.0", port=5000)