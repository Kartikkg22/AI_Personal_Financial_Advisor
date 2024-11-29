from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import mysql.connector
import yfinance as yf
from transformers import pipeline
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
from datetime import datetime
import pandas as pd
import mplfinance as mpf
import os
from db_connection import get_db_connection

app = Flask(__name__)
CORS(app)

@app.route('/api/candlestick-chart', methods=['GET'])
def get_candlestick_chart():
    # Path to the Excel file (replace with your actual file path)
    excel_file_path = "real_time_stock_data.xlsx"
    
    # Check if the file exists
    if not os.path.exists(excel_file_path):
        return {"error": "Excel file not found"}, 404

    try:
        # Read the Excel file
        data = pd.read_excel(excel_file_path)

        # Validate required columns
        required_columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        if not all(column in data.columns for column in required_columns):
            return {"error": f"Excel file must contain the following columns: {required_columns}"}, 400

        # Convert 'Date' to datetime and set as index
        data["Date"] = pd.to_datetime(data["Date"])
        data.set_index("Date", inplace=True)

        # Generate the candlestick chart
        chart_file_path = "static/candlestick_chart.png"  # Save chart as PNG
        mpf.plot(data, type="candle", style="charles", volume=True, 
                 title="Stock Prices", ylabel="Price (INR)", savefig=chart_file_path)

        # Return the chart as a static image
        return send_file(chart_file_path, mimetype="image/png")

    except Exception as e:
        return {"error": str(e)}, 500


# Example route for checking server status
@app.route('/api/status', methods=['GET'])
def status():
    return {"status": "Server is running"}

# API endpoint for user authentication
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json  # Get JSON data from the request
    username = data.get('username')
    password = data.get('password')

    # Validate input
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if the user exists and the password matches
    cursor.execute("SELECT * FROM users WHERE email = %s AND password_hash = %s", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful", "user": user}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json  # Get JSON data from the request
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')  # Ensure this is hashed before storing
    income = data.get('income', 0.0)

    # Validate input
    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Insert the new user into the database
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, income)
            VALUES (%s, %s, %s, %s)
        """, (name, email, password, income))  # Replace with hashed password
        conn.commit()
        return jsonify({"message": "Signup successful"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409
    finally:
        conn.close()

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch user details by user_id
    cursor.execute("SELECT id, name, email, income, expenses, savings FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/complete-profile', methods=['POST'])
def complete_profile():
    data = request.json
    user_id = data.get('userId')
    income = data.get('income')
    expenses = data.get('expenses')
    savings = data.get('savings')
    goals = data.get('goals')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE users
            SET income = %s, expenses = %s, savings = %s, goals = %s
            WHERE id = %s
        """, (income, expenses, savings, goals, user_id))
        conn.commit()
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/market-data', methods=['GET'])
def get_market_data():
    # Fetch real-time data for major indices
    indices = {
        "S&P 500": "^GSPC",
        "NASDAQ": "^IXIC",
        "Dow Jones": "^DJI"
    }

    market_data = []
    for name, symbol in indices.items():
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="1d")  # Fetch daily data
        current_price = history["Close"].iloc[-1]
        prev_close = history["Close"].iloc[-2]
        change = ((current_price - prev_close) / prev_close) * 100
        market_data.append({
            "name": name,
            "value": round(current_price, 2),
            "change": round(change, 2)
        })

    return jsonify({"indices": market_data}), 200

@app.route('/api/ai-insights', methods=['GET'])
def get_ai_insights():
    # Dummy AI insights (replace with actual AI model predictions)
    insights = [
        {"stock": "Apple", "sentiment": "Positive", "prediction": "Uptrend", "risk": "Low"},
        {"stock": "Tesla", "sentiment": "Neutral", "prediction": "Stable", "risk": "Medium"},
        {"stock": "Amazon", "sentiment": "Negative", "prediction": "Downtrend", "risk": "High"}
    ]
    return jsonify({"insights": insights}), 200

@app.route('/api/user/<int:user_id>/portfolio', methods=['GET'])
def get_user_portfolio(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id, asset_name AS name, amount AS invested, 
                   amount * 1.05 AS currentValue, 
                   (1.05 - 1) * 100 AS change 
            FROM investment_portfolio 
            WHERE user_id = %s
        """, (user_id,))
        portfolio = cursor.fetchall()
        return jsonify({"portfolio": portfolio}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/portfolio', methods=['POST'])
def add_to_portfolio():
    data = request.json
    user_id = data.get('userId')
    stock = data.get('stock')
    amount = data.get('amount')

    if not user_id or not stock or not amount:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO investment_portfolio (user_id, asset_name, amount, date_of_investment)
            VALUES (%s, %s, %s, %s)
        """, (user_id, stock, amount, datetime.now()))
        conn.commit()
        return jsonify({"message": "Stock added to portfolio successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/price-alert', methods=['POST'])
def set_price_alert():
    data = request.json
    user_id = data.get('userId')
    stock = data.get('stock')
    target_price = data.get('targetPrice')

    if not user_id or not stock or not target_price:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO price_alerts (user_id, stock_name, target_price)
            VALUES (%s, %s, %s)
        """, (user_id, stock, target_price))
        conn.commit()
        return jsonify({"message": "Price alert set successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/market-news', methods=['GET'])
def get_market_news():
    # Simulate news headlines (replace with live API like NewsAPI)
    news_data = [
        {"title": "Apple's Earnings Beat Expectations", "summary": "Apple reported strong quarterly earnings...", "link": "https://example.com/apple-news"},
        {"title": "Tesla Expands into New Markets", "summary": "Tesla plans to open factories in Asia...", "link": "https://example.com/tesla-news"},
        {"title": "Amazon Faces Revenue Decline", "summary": "Amazon's revenue fell by 5% in the last quarter...", "link": "https://example.com/amazon-news"}
    ]

    # Add sentiment analysis for each news headline
    for article in news_data:
        sentiment_result = sentiment_model(article["summary"])[0]
        article["sentiment"] = sentiment_result["label"]

    return jsonify({"news": news_data}), 200

# Initialize sentiment analysis pipeline
sentiment_model = pipeline("sentiment-analysis")

if __name__ == '__main__':
    app.run(debug=True)
