from flask import Flask
from flask import session
from flask import redirect, url_for
from flask import request
import socket

app = Flask(__name__)
app.secret_key = 'supersecretkey'

visitor_count = 0

@app.route('/')
def index():
    global visitor_count
    if 'visited' not in session:
        session['visited'] = True
        visitor_count += 1
    return f"Visitor count: {visitor_count}"

 
@app.route("/hostname")
def get_hostname():
    hostname = socket.gethostname()
    return f"Hostname :: {hostname}"

@app.route("/request-url")
def request_url():
    return f"Request URL: {request.url}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)