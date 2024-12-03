from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from db_connection import get_db_connection
from transformers import pipeline
from datetime import datetime,timedelta
import yfinance as yf
import numpy as np
from io import BytesIO
from sklearn.linear_model import LinearRegression
import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app)

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
def add_portfolio():
    data = request.json
    user_id = data.get('userId')
    portfolio = data.get('portfolio')

    if not user_id or not portfolio:
        return jsonify({"error": "User ID and portfolio data are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        for stock in portfolio:
            cursor.execute("""
                INSERT INTO investment_portfolio (user_id, asset_name, amount, date_of_investment)
                VALUES (%s, %s, %s, %s)
            """, (user_id, stock['name'], stock['amount'], stock['date']))
        conn.commit()
        return jsonify({"message": "Portfolio updated successfully"}), 201
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

def load_company_data(company_name):
    try:
        file_paths = {
            "Infosys": "infosys_data.xlsx",
            "Wipro": "wipro_data.xlsx",
            "Tata Steel": "tata_steel_data.xlsx",
            "Zomato": "zomato_data.xlsx",
        }

        if company_name not in file_paths:
            return None

        # Read the Excel file
        df = pd.read_excel(file_paths[company_name])

        # Debug: Print columns to verify
        print(f"Columns in {company_name} dataset: {df.columns.tolist()}")

        # Ensure the required columns exist
        if "Date" not in df.columns or "Low" not in df.columns:
            raise ValueError(f"Dataset for {company_name} is missing required columns: 'Date' or 'Close'")

        # Parse 'Date' column with the format 'DD-MM-YYYY'
        df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce")

        # Drop rows with invalid dates
        df = df.dropna(subset=["Date"])

        # Sort data by date
        df = df.sort_values("Date")

        return df

    except Exception as e:
        print(f"Error loading data for {company_name}: {e}")
        return None

def predict_future_prices(data, future_days=10):
    """
    Predict future stock prices using Linear Regression.
    Args:
        data (pd.DataFrame): DataFrame with 'Date' and 'Close' columns.
        future_days (int): Number of days to predict.
    Returns:
        predicted_dates (list): List of future dates.
        predictions (list): List of predicted prices.
    """
    # Convert dates to numerical values for regression
    data["Day"] = (data["Date"] - data["Date"].min()).dt.days

    # Features and target
    X = data[["Day"]]
    y = data["Low"]

    # Train Linear Regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict future values
    last_day = data["Day"].iloc[-1]
    predicted_days = np.arange(last_day + 1, last_day + future_days + 1).reshape(-1, 1)
    predictions = model.predict(predicted_days)

    # Generate corresponding dates for predictions
    last_date = data["Date"].iloc[-1]
    predicted_dates = [last_date + timedelta(days=i) for i in range(1, future_days + 1)]

    return predicted_dates, predictions

# Route to generate candlestick chart
@app.route("/api/line-chart/<company_name>", methods=["GET"])
def generate_line_chart(company_name):
    df = load_company_data(company_name)
    if df is None:
        return jsonify({"error": "Invalid company name or data unavailable"}), 400

    # Generate line chart
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot Date vs Close price
    ax.plot(df["Date"], df["Low"], color="blue", marker="o", linestyle="-", linewidth=2, markersize=4)

    # Add labels and title
    ax.set_title(f"Line Chart - {company_name} Closing Prices", fontsize=16)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Closing Price (INR)", fontsize=12)
    ax.grid(visible=True, linestyle="--", alpha=0.7)

    # Format x-axis for better readability
    plt.xticks(rotation=45, fontsize=10)
    plt.tight_layout()

    # Save plot to a BytesIO stream
    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close(fig)

    return send_file(img, mimetype="image/png")

@app.route('/api/predict/<company_name>', methods=['GET'])
def predict_company_stock(company_name):
    df = load_company_data(company_name)
    if df is None:
        return jsonify({"error": "Invalid company name or data unavailable"}), 400

    # Use your prediction function (e.g., Linear Regression)
    future_dates, predicted_prices = predict_future_prices(df, future_days=10)

    # Determine the trend
    trend = "Upward" if predicted_prices[-1] > predicted_prices[0] else "Downward"

    # Prepare JSON response
    predictions = [{"date": future_dates[i].strftime("%d-%m-%Y"), "price": predicted_prices[i]} for i in range(len(future_dates))]
    return jsonify({"predictions": predictions, "trend": trend})

def recommend_investments(user_id, portfolio, future_predictions):
    """
    Generate investment recommendations based on the user's portfolio and predictions.
    Args:
        user_id (int): User ID.
        portfolio (list): List of user's current investments.
        future_predictions (dict): Predicted stock prices.
    Returns:
        list: Recommendations for investments.
    """
    recommendations = []

    for stock in portfolio:
        stock_name = stock["name"]
        current_price = float(stock["amount"])  # Convert Decimal to float
        target_price = current_price * 1.2  # Example target: 20% growth

        # Fetch future prediction for this stock
        predicted_data = future_predictions.get(stock_name)
        print(predicted_data)
        if predicted_data:
            predicted_prices = predicted_data["predicted_prices"]
            trend = predicted_data["trend"]
            
            # Provide recommendation based on trend
            if trend == "Upward":
                recommendations.append({
                    "stock": stock_name,
                    "current_price": current_price,
                    "target_price": target_price,
                    "status": "Recommended",
                    "reason": f"The stock is predicted to go upwards. Consider buying."
                })
            elif trend == "Downward":
                recommendations.append({
                    "stock": stock_name,
                    "current_price": current_price,
                    "target_price": target_price,
                    "status": "Not Recommended",
                    "reason": f"The stock is predicted to go downwards. Consider selling or avoiding."
                })
            else:
                recommendations.append({
                    "stock": stock_name,
                    "current_price": current_price,
                    "target_price": target_price,
                    "status": "Neutral",
                    "reason": f"The stock trend is stable. Hold off on major decisions."
                })
        else:
            # If predictions are not available, provide a default recommendation
            recommendations.append({
                "stock": stock_name,
                "current_price": current_price,
                "target_price": target_price,
                "status": "No Prediction Available",
                "reason": f"No predictions are available for {stock_name}."
            })

    return recommendations


@app.route('/api/recommendations/<int:user_id>', methods=['GET'])
def portfolio_recommendations(user_id):
    # Fetch the user's portfolio
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT asset_name AS name, amount, amount * 1.05 AS currentValue
        FROM investment_portfolio
        WHERE user_id = %s
    """, (user_id,))
    portfolio = cursor.fetchall()

    print("User Portfolio:", portfolio)

    # Fetch predictions for each stock in the portfolio
    future_predictions = {}
    for stock in portfolio:
        stock_name = stock["name"]
        df = load_company_data(stock_name)  # Load company data for each stock
        print(df)
        if df is not None:
            # Predict future prices for this stock
            future_dates, predicted_prices = predict_future_prices(df, future_days=10)
            trend = "Upward" if predicted_prices[-1] > predicted_prices[0] else "Downward"

            # Store predictions and trend for each stock in the future_predictions dictionary
            future_predictions[stock_name] = {
                "predicted_prices": predicted_prices,
                "trend": trend
            }
        else:
            print(f"Error loading data for {stock_name}")

    print("Future Predictions:", future_predictions)

    # Generate recommendations
    recommendations = recommend_investments(user_id, portfolio, future_predictions)

    # Close database connection
    conn.close()

    # Return portfolio and recommendations as JSON
    return jsonify({"portfolio": portfolio, "recommendations": recommendations})

if __name__ == '__main__':
    app.run(debug=True)
