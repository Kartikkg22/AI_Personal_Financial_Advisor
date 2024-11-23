from backend.app import app
from flask import jsonify

@app.route('/summary', methods=['GET'])
def get_summary():
    # Replace with actual database queries or AI model predictions
    data = {
        "expenses": "$1,200",
        "savings": "$800"
    }
    return jsonify(data)


@app.route('/')
def home():
    return jsonify(message="AI Personal Financial Advisor API is running!")
