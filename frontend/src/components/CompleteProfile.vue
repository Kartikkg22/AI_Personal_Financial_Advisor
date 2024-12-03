<template>
  <div class="complete-profile-page">
    <h1>Complete Your Profile</h1>
    <form @submit.prevent="handleSubmit">
      <!-- Income Field -->
      <div class="form-group">
        <label for="income">Income</label>
        <input type="number" id="income" v-model="income" placeholder="Enter your income" required />
      </div>

      <!-- Expenses Field -->
      <div class="form-group">
        <label for="expenses">Expenses</label>
        <input type="number" id="expenses" v-model="expenses" placeholder="Enter your expenses" required />
      </div>

      <!-- Savings Field -->
      <div class="form-group">
        <label for="savings">Savings</label>
        <input type="number" id="savings" v-model="savings" placeholder="Enter your savings" required />
      </div>

      <!-- Goals Field -->
      <div class="form-group">
        <label for="goals">Goals (e.g., retirement, vacation)</label>
        <textarea id="goals" v-model="goals" placeholder="Enter your financial goals"></textarea>
      </div>

      <!-- Portfolio Section -->
      <h2>Add Your Portfolio</h2>
      <div v-for="(stock, index) in portfolio" :key="index" class="portfolio-group">
        <div class="form-group">
          <label>Stock Name</label>
          <input type="text" v-model="stock.name" placeholder="Enter stock name" required />
        </div>
        <div class="form-group">
          <label>Investment Amount</label>
          <input type="number" v-model="stock.amount" placeholder="Enter investment amount" required />
        </div>
        <div class="form-group">
          <label>Date of Investment</label>
          <input type="date" v-model="stock.date" required />
        </div>
        <button type="button" @click="removeStock(index)" class="btn btn-secondary">Remove Stock</button>
      </div>
      <button type="button" @click="addStock" class="btn btn-secondary">Add Another Stock</button>

      <!-- Submit Button -->
      <button type="submit" class="btn btn-primary">Save Profile</button>
    </form>

    <p v-if="message" :class="messageClass">{{ message }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CompleteProfile",
  data() {
    return {
      income: "",
      expenses: "",
      savings: "",
      goals: "",
      portfolio: [
        { name: "", amount: "", date: "" }, // Default single stock entry
      ],
      message: null,
      messageClass: null, // To indicate success or error
    };
  },
  methods: {
    addStock() {
      this.portfolio.push({ name: "", amount: "", date: "" });
    },
    removeStock(index) {
      this.portfolio.splice(index, 1);
    },
    async handleSubmit() {
      const userId = localStorage.getItem("userId");
      if (!userId) {
        this.message = "You need to log in to complete your profile.";
        this.messageClass = "error";
        return;
      }

      try {
        // Save user profile data
        await axios.post(`http://127.0.0.1:5000/api/complete-profile`, {
          userId,
          income: this.income,
          expenses: this.expenses,
          savings: this.savings,
          goals: this.goals,
        });

        // Save stock portfolio data
        await axios.post(`http://127.0.0.1:5000/api/portfolio`, {
          userId,
          portfolio: this.portfolio,
        });

        this.message = "Profile and portfolio updated successfully!";
        this.messageClass = "success";

        // Clear the form fields
        this.income = "";
        this.expenses = "";
        this.savings = "";
        this.goals = "";
        this.portfolio = [{ name: "", amount: "", date: "" }];

        // Redirect to the profile page
        setTimeout(() => {
          this.$router.push("/profile");
        }, 2000);
      } catch (error) {
        console.error(error);
        this.message = "An error occurred while updating your profile or portfolio. Please try again.";
        this.messageClass = "error";
      }
    },
  },
};
</script>

<style scoped>
.complete-profile-page {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    text-align: left;
  }
  
  h1 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  input, textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    margin-top: 20px;
    width: 100%;
    padding: 10px;
    background-color: #1976d2;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #155a9e;
  }
  
  .success {
    color: green;
    text-align: center;
  }
  
  .error {
    color: red;
    text-align: center;
  }

  .portfolio-group {
    border: 1px solid #ccc;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 4px;
  }
  .btn-secondary {
    margin-top: 10px;
    background-color: #6c757d;
    color: white;
    padding: 8px 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
</style>
