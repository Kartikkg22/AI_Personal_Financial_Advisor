from flask import Flask, jsonify, send_file
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from io import BytesIO

app = Flask(__name__)

# Path to Excel files
EXCEL_FILES = {
    "Zomato": "zomato_data.xls",
    "Infosys": "infosys_data.xls",
    "Wipro": "wipro_data.xls",
    "Tata Steel": "tata_steel_data.xls",
}

# Function to load company data
def load_company_data(company_name):
    try:
        # Check if the company exists in the data source
        if company_name not in EXCEL_FILES:
            return None
        
        # Read the corresponding Excel file for the company
        df = pd.read_excel(EXCEL_FILES[company_name])
        df["Date"] = pd.to_datetime(df["Date"])  # Ensure 'Date' is in datetime format
        return df

    except Exception as e:
        print(f"Error loading data for {company_name}: {e}")
        return None

# Route to generate candlestick chart
@app.route("/api/line-chart/<company_name>", methods=["GET"])
def generate_line_chart(company_name):
    df = load_company_data(company_name)
    if df is None:
        return jsonify({"error": "Invalid company name or data unavailable"}), 400

    # Generate line chart
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot Date vs Close price
    ax.plot(df["Date"], df["Close"], color="blue", marker="o", linestyle="-", linewidth=2, markersize=4)

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



if __name__ == "__main__":
    app.run(debug=True)
