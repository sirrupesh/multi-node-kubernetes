"""
Flask Application for Kubernetes Demo
Features:
- Visit tracking with session management
- Pod identification for cluster debugging
- Request inspection for troubleshooting
- Health check endpoints for production monitoring
- Designed for high availability deployment
"""

from flask import Flask, session, request
import socket
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

visitor_count = 0  # Global counter for unique visitors

# Health check statuses
is_ready = True
is_live = True

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

@app.route("/health/live")
def liveness():
    """
    Liveness probe endpoint for Kubernetes.
    Indicates whether the application is running and responsive.
    """
    if is_live:
        return {"status": "healthy"}, 200
    return {"status": "unhealthy"}, 500

@app.route("/health/ready")
def readiness():
    """
    Readiness probe endpoint for Kubernetes.
    Indicates whether the application is ready to handle traffic.
    """
    if is_ready:
        return {"status": "ready"}, 200
    return {"status": "not ready"}, 503

# Add metrics endpoint if metrics are enabled
if os.getenv('ENABLE_METRICS', 'false').lower() == 'true':
    from prometheus_client import generate_latest, Counter, CONTENT_TYPE_LATEST
    
    # Define metrics
    REQUESTS = Counter('http_requests_total', 'Total HTTP Requests')
    VISITORS = Counter('unique_visitors_total', 'Total Unique Visitors')
    
    @app.route('/metrics')
    def metrics():
        """
        Prometheus metrics endpoint.
        Exposes application metrics for monitoring.
        """
        return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    # Set default port for container networking
    port = int(os.getenv('PORT', 5000))
    # Enable debug mode in development
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
    app.run(host="0.0.0.0", port=port, debug=debug)