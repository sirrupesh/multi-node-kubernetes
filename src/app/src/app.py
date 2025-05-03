"""
Flask app for visit tracking and cluster diagnostics
- Session-based visitor counting
- Pod and request inspection
- Health monitoring endpoints
"""

from flask import Flask, session, request
import socket
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management

visitor_count = 0  # Global visit counter

# Health states
is_ready = True
is_live = True

@app.route('/')
def index():
    """Track unique visitors using session cookies"""
    global visitor_count
    if 'visited' not in session:
        session['visited'] = True
        visitor_count += 1
    return f"Visitor count: {visitor_count}"

@app.route("/hostname")
def get_hostname():
    """Return pod hostname for K8s deployment verification"""
    hostname = socket.gethostname()
    return f"Hostname :: {hostname}"

@app.route("/request-url")
def request_url():
    """Debug endpoint for request inspection"""
    return f"Request URL: {request.url}"

@app.route("/health/live")
def liveness():
    """K8s liveness probe endpoint"""
    if is_live:
        return {"status": "healthy"}, 200
    return {"status": "unhealthy"}, 500

@app.route("/health/ready")
def readiness():
    """K8s readiness probe endpoint"""
    if is_ready:
        return {"status": "ready"}, 200
    return {"status": "not ready"}, 503

# Optional metrics endpoint
if os.getenv('ENABLE_METRICS', 'false').lower() == 'true':
    from prometheus_client import generate_latest, Counter, CONTENT_TYPE_LATEST
    
    REQUESTS = Counter('http_requests_total', 'Total HTTP Requests')
    VISITORS = Counter('unique_visitors_total', 'Total Unique Visitors')
    
    @app.route('/metrics')
    def metrics():
        """Expose Prometheus metrics"""
        return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
    app.run(host="0.0.0.0", port=port, debug=debug)