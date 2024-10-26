from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/financial-advice', methods=['POST'])
def financial_advice():
    data = request.json
    # Simple example of financial advice logic
    advice = "Start saving at least 20% of your income!"
    return jsonify({"advice": advice})

if __name__ == '__main__':
    app.run(debug=True)
