<template>
  <div class="container">
    <header>
      <img src="@/assets/logo.png" alt="logo of the website">
      <h1>Welcome to AI Personal Financial Advisor</h1>
      <p>Take control of your finances with smart insights and recommendations.</p>
    </header>

    
    <nav>
      <router-link  href="#" :to="{name: 'StockMarketPage'}"class="btn btn-primary" @click="gotoStockMarket" >Go to Stock Market</router-link>
      <router-link href="#" :to="{name : 'ProfilePage'}" class="btn btn-secondary" @click ="gotoProfile">View Profile</router-link>
      <router-link  class="btn btn-success">See Reports</router-link>
      <router-link href="#" :to="{name : 'CompleteProfile'}" class="btn btn-warning" @click="gotoCompleteProfile">Complete Profile</router-link>
    </nav>

    <section v-if="summary" class="financial-summary">
      <h2>Your Financial Summary</h2>
      <p>Total Expenses This Month: <strong>{{ summary.expenses }}</strong></p>
      <p>Total Savings This Month: <strong>{{ summary.savings }}</strong></p>
    </section>

    <section v-else class="loading-summary">
      <p>Loading your financial summary...</p>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      summary: null, // Sample financial summary data
      isAuthenticated: localStorage.getItem("isAuthenticated") === "true",
      user: localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : null,
    };
  },
  mounted() {
    // Simulate fetching financial summary data
  },
  methods :{
    gotoProfile(){
      this.$router.push({ name : "ProfilePage"})
    },
    gotoCompleteProfile(){
      this.$router.push({ name: "CompleteProfile" })
    },
    gotoStockMarket(){
      this.$router.push({ name: "StockMarketPage"})
    },
    logout() {
      localStorage.removeItem("isAuthenticated");
      localStorage.removeItem("user");
      this.isAuthenticated = false;
      this.user = null;
      this.$router.push("/login");
    },
  }
};
</script>

<style scoped>
/* General Layout */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
  justify-content: center;
  align-items: center;
}

/* Header Section */
header {
  background-color: #1976D2;
  color: white;
  padding: 40px 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

header h1 {
  font-size: 2.5em;
  margin-bottom: 10px;
}

header img {
  width: 100px;  /* Adjust size as needed */
  height: auto;
  margin-bottom: 20px;
}

header p {
  font-size: 1.2em;
}

/* Navigation Section */
nav {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 40px;
}

.btn {
  padding: 15px 30px;
  font-size: 1.1em;
  text-decoration: none;
  border-radius: 4px;
  display: inline-block;
  transition: background-color 0.3s ease;
}

.btn-primary {
  background-color: #757575;
  color: white;
}

.btn-secondary {
  background-color: #757575;
  color: white;
}

.btn-success {
  background-color: #757575;
  color: white;
}

.btn-warning{
  background-color: #757575;
  color: white;
}

/* Hover Effects for Buttons */
.btn:hover {
  opacity: 0.9;
}

/* Financial Summary Section */
.financial-summary {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.financial-summary h2 {
  font-size: 1.8em;
  margin-bottom: 15px;
}

.financial-summary p {
  font-size: 1.2em;
}

.financial-summary strong {
  font-size: 1.3em;
  color: #1976D2;
}

/* Loading Section */
.loading-summary {
  font-size: 1.2em;
  color: #757575;
}

/* Responsiveness for Smaller Screens */
@media (max-width: 768px) {
  .nav {
    flex-direction: column;
  }

  .btn {
    width: 100%;
    margin-bottom: 10px;
  }
}
</style>
