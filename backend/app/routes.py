from backend.app import app
from flask import jsonify

@app.route('/')
def home():
    return jsonify(message="AI Personal Financial Advisor API is running!")
