from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import sys

# Add the project root to sys.path so that 'backend' module can be found
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from backend.api.routes import api_blueprint

# Define directories relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/static")

# Configure CORS so the frontend can communicate with the backend
CORS(app)

# Register the API routes
app.register_blueprint(api_blueprint)


@app.route("/")
def root():
    return send_from_directory(STATIC_DIR, "index.html")

if __name__ == "__main__":
    # Flask's built-in development server
    app.run(host="0.0.0.0", port=4000, debug=True)

