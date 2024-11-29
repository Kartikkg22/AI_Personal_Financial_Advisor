<template>
    <div class="stock-market-page">
      <!-- Left Sidebar -->
      <aside class="sidebar">
        <nav>
          <ul>
            <li><a href="#">Trades</a></li>
            <li><a href="#">Market</a></li>
            <li><a href="#">Events</a></li>
            <li><a href="#">Help</a></li>
          </ul>
        </nav>
      </aside>
  
      <!-- Main Content -->
      <main class="chart-section">
        <header>
          <h2>Stock Market</h2>
          <p>Selected Stock: {{ selectedStock.name }} | FT: {{ selectedStock.performance }}</p>
        </header>
        <div class="candlestick-chart">
      <h2>Candlestick Chart</h2>
      <img 
        v-if="chartUrl" 
        :src="chartUrl" 
        alt="Candlestick Chart" 
        class="chart-image"
      />
      <p v-else>Loading chart...</p>
    </div>

    <!-- Add other sections for portfolio and alerts -->
    <div class="portfolio-section">
      <h2>Your Portfolio</h2>
      <!-- Add Portfolio UI here -->
    </div>

    <div class="alerts-section">
      <h2>Set Price Alerts</h2>
      <!-- Add Alert UI here -->
    </div>
      </main>
  
      <!-- Right Sidebar -->
      <aside class="controls">
        <div class="account-info">
          <h3>Account: {{ account.balance }}</h3>
          <button class="payments-btn">Payments</button>
        </div>
        <div class="trade-settings">
          <h4>Trade Settings</h4>
          <div>
            <label>Amount, INR</label>
            <input type="number" v-model="trade.amount" />
          </div>
          <div>
            <label>Duration</label>
            <input type="number" v-model="trade.duration" /> min
          </div>
        </div>
        <div class="trade-actions">
          <button class="up-btn" @click="placeTrade('up')">Up</button>
          <button class="down-btn" @click="placeTrade('down')">Down</button>
        </div>
      </aside>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        chartUrl: null,
        selectedStock: {
          name: "Amazon",
          performance: "85%"
        },
        account: {
          balance: "INR 0.00"
        },
        trade: {
          amount: 0,
          duration: 1 // in minutes
        },
        chart: null
      };
    },
    mounted() {
        this.fetchCandlestickChart(); // Fetch the chart when the page loads
    },
    methods: {
        fetchCandlestickChart() {
            const apiUrl = "http://localhost:5000/api/candlestick-chart"; // Update with your backend URL
            this.chartUrl = apiUrl; // Point to the backend API for the candlestick chart
        },
  
        placeTrade(direction) {
            alert(`Placing ${direction} trade for ${this.trade.amount} INR.`);
            // Backend integration logic
        }
    }
  };
  </script>
  
  <style scoped>
  .stock-market-page {
    display: flex;
    height: 100vh;
  }
  
  .sidebar {
    width: 15%;
    background: #1a1a1a;
    color: #fff;
    padding: 20px;
  }
  
  .sidebar nav ul {
    list-style-type: none;
    padding: 0;
  }
  
  .sidebar nav ul li a {
    color: #fff;
    text-decoration: none;
    display: block;
    padding: 10px 0;
  }
  
  .candlestick-chart {
    text-align: center;
    margin-bottom: 40px;
  }

  .chart-image {
    width: 100%;
    max-width: 800px;
    height: auto;
    border: 1px solid #ccc;
  }

  
  .chart-section header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
  }
  
  #chart-container {
    background: #000;
    padding: 20px;
    border-radius: 8px;
  }
  
  .controls {
    width: 15%;
    background: #202020;
    color: #fff;
    padding: 20px;
  }
  
  .controls h3,
  .controls h4 {
    margin: 10px 0;
  }
  
  .payments-btn {
    display: block;
    margin: 10px 0;
    padding: 10px;
    background: #28a745;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .trade-actions button {
    width: 48%;
    padding: 10px;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .up-btn {
    background: #28a745;
  }
  
  .down-btn {
    background: #dc3545;
  }
  </style>
  