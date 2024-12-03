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
        <p>Selected Stock: {{ selectedStock.name }} | Performance: {{ selectedStock.performance }}</p>
      </header>

      <!-- Line Chart -->
      <div class="line-chart">
        <h2>Stock Price Chart - {{ selectedStock.name }}</h2>
        <img
          v-if="chartUrl"
          :src="chartUrl"
          alt="Line Chart"
          class="chart-image"
        />
        <p v-else>Loading chart...</p>
      </div>

      <!-- Portfolio Section -->
      <div class="portfolio-section">
        <h2>Your Portfolio</h2>
        <p>Manage and track your investments here.</p>
      </div>

      <!-- Alerts Section -->
      <div class="alerts-section">
        <h2>Set Price Alerts</h2>
        <p>Configure your alerts based on price thresholds.</p>
      </div>
    </main>

    <!-- Right Sidebar -->
    <aside class="controls">
      <!-- Trade Settings -->
      <div class="trade-settings">
        <h4>Trade Settings</h4>

        <!-- Dropdown for selecting a company -->
        <div>
          <label for="company">Select Company:</label>
          <select id="company" v-model="selectedCompany" @change="fetchCompanyData">
            <option disabled value="">-- Choose a Company --</option>
            <option v-for="company in companies" :key="company.name" :value="company.name">
              {{ company.name }}
            </option>
          </select>
        </div>

        <!-- Trade Amount and Duration -->
        <div>
          <label>Amount (INR)</label>
          <input type="number" v-model="trade.amount" />
        </div>
        <div>
          <label>Duration</label>
          <input type="number" v-model="trade.duration" /> min
        </div>

        <!-- Trade Actions -->
        <div class="trade-actions">
          <button class="up-btn" @click="placeTrade('up')">Up</button>
          <button class="down-btn" @click="placeTrade('down')">Down</button>
        </div>
      </div>

      <!-- Account Balance -->
      <div class="account-info">
        <h3>Account Balance</h3>
        <p>{{ account.balance }}</p>
        <button class="payments-btn">Payments</button>
      </div>
    </aside>
  </div>
</template>

<script>
export default {
  data() {
    return {
      companies: [
        { name: "Infosys", performance: "75%" },
        { name: "Wipro", performance: "80%" },
        { name: "Zomato", performance: "85%" },
        { name: "Tata Steel", performance: "70%" },
      ],
      selectedCompany: "Zomato", // Default selected company
      chartUrl: null, // URL for the line chart
      selectedStock: {
        name: "Zomato",
        performance: "85%",
      },
      account: {
        balance: "INR 10,000.00",
      },
      trade: {
        amount: 0,
        duration: 1, // in minutes
      },
    };
  },
  mounted() {
    this.fetchCompanyData(); // Fetch initial data for the default selected company
  },
  methods: {
    async fetchCompanyData() {
      try {
        // Update the selected stock details dynamically
        const stock = this.companies.find((company) => company.name === this.selectedCompany);
        if (stock) {
          this.selectedStock = stock;
        }

        // Fetch Line Chart from the backend (Python server)
        const apiUrl = `http://localhost:5000/api/line-chart/${this.selectedCompany}`; // Updated API endpoint
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error("Failed to fetch the line chart");
        }
        const blob = await response.blob(); // Get image as blob
        this.chartUrl = URL.createObjectURL(blob); // Convert to local object URL
      } catch (error) {
        console.error("Error fetching company data:", error);
      }
    },
    placeTrade(direction) {
      alert(`Placing a ${direction} trade for ${this.trade.amount} INR on ${this.selectedCompany}.`);
      // Add trade backend integration logic here
    },
  },
};
</script>

<style scoped>
/* Fullscreen Layout */
.stock-market-page {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* Sidebar */
.sidebar {
  width: 15%;
  background: #1a1a1a;
  color: #fff;
  padding: 20px;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  box-sizing: border-box;
  height: 100%;
  overflow-y: auto;
}

.sidebar nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar nav ul li a {
  color: #fff;
  text-decoration: none;
  display: block;
  padding: 10px 0;
}

/* Main Content */
.chart-section {
  margin-left: 15%; /* Make room for the sidebar */
  padding: 20px;
  background: #f5f5f5;
  overflow-y: auto;
  box-sizing: border-box;
  width: 85%; /* Full width minus the sidebar */
  height: 100%;
}

.chart-section header {
  margin-bottom: 20px;
  text-align: center;
}

.line-chart {
  text-align: center;
  margin-bottom: 40px;
}

.chart-image {
  width: 100%;
  max-width: 100%;
  height: auto;
  border: 1px solid #ccc;
  border-radius: 8px;
}

/* Controls Section */
.controls {
  width: 15%;
  background: #202020;
  color: #fff;
  padding: 20px;
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  box-sizing: border-box;
  height: 100%;
  overflow-y: auto;
}

.controls h3,
.controls h4 {
  margin-bottom: 10px;
}

.payments-btn {
  padding: 10px;
  background: #28a745;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.trade-settings label {
  display: block;
  margin-bottom: 5px;
}

.trade-actions button {
  width: 48%;
  margin-top: 10px;
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

/* Responsive Design */
@media (max-width: 1024px) {
  .stock-market-page {
    flex-wrap: wrap; /* Stack sections vertically */
  }

  .sidebar,
  .controls {
    width: 100%; /* Full width for sidebar and controls */
    margin-bottom: 20px;
  }

  .chart-section {
    width: 100%; /* Full width for the chart section */
    margin-left: 0;
  }

  .line-chart img {
    max-width: 90%;
  }
}

@media (max-width: 768px) {
  .sidebar nav ul li a {
    font-size: 0.9em;
    padding: 8px 0;
  }

  .controls {
    padding: 15px;
  }

  .trade-settings label,
  .controls h4 {
    font-size: 0.9em;
  }
}

@media (max-width: 480px) {
  .line-chart img {
    max-width: 100%;
  }

  .trade-actions button {
    width: 100%;
    margin-bottom: 10px;
  }
}
</style>
