from flask import Flask

app = Flask(__name__)

from backend.app import routes  # Import routes after initializing the app
