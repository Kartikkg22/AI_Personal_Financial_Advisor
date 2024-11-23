from flask import Flask, jsonify
from flask_cors import CORS
from db_connection import get_db_connection

app = Flask(__name__)
CORS(app)

# API endpoint to fetch profile data
@app.route('/api/profile', methods=['GET'])
def get_profile():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name, email FROM users WHERE id = 1") # Example query
    profile = cursor.fetchone()
    print("profile data ",profile)
    conn.close()
    # API route to fetch profile data

    return jsonify(profile)  # Return profile as JSON

if __name__ == '__main__':
    app.run(debug=True)
