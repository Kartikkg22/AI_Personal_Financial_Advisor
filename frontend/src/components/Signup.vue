<template>
    <div class="signup-page">
      <div class="signup-container">
        <h1>Sign Up</h1>
        <form @submit.prevent="handleSignup">
          <!-- Name Field -->
          <div class="form-group">
            <label for="name">Full Name</label>
            <input
              type="text"
              id="name"
              v-model="name"
              placeholder="Enter your full name"
              required
            />
          </div>
  
          <!-- Email Field -->
          <div class="form-group">
            <label for="email">Email</label>
            <input
              type="email"
              id="email"
              v-model="email"
              placeholder="Enter your email"
              required
            />
          </div>
  
          <!-- Password Field -->
          <div class="form-group">
            <label for="password">Password</label>
            <input
              type="password"
              id="password"
              v-model="password"
              placeholder="Enter your password"
              required
            />
          </div>
  
          <!-- Income Field -->
          <div class="form-group">
            <label for="income">Monthly Income</label>
            <input
              type="number"
              id="income"
              v-model="income"
              placeholder="Enter your monthly income"
            />
          </div>
  
          <!-- Submit Button -->
          <button type="submit" class="btn">Sign Up</button>
        </form>
  
        <!-- Error or Success Message -->
        <p v-if="message" :class="messageClass">{{ message }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "SignupPage",
    data() {
      return {
        name: "",
        email: "",
        password: "",
        income: "",
        message: null,
        messageClass: null, // Class for success or error message
      };
    },
    methods: {
      async handleSignup() {
        try {
          // Make a POST request to the backend
          const response = await axios.post("http://127.0.0.1:5000/api/signup", {
            name: this.name,
            email: this.email,
            password: this.password,
            income: this.income,
          });
  
          // Display success message
          this.message = response.data.message;
          this.messageClass = "success";
          this.resetForm();
  
          // Redirect to the login page after a short delay
          setTimeout(() => {
            this.$router.push("/login");
          }, 2000);
        } catch (error) {
          // Display error message
          if (error.response && error.response.data) {
            this.message = error.response.data.error;
          } else {
            this.message = "An unexpected error occurred. Please try again.";
          }
          this.messageClass = "error";
        }
      },
      resetForm() {
        this.name = "";
        this.email = "";
        this.password = "";
        this.income = "";
      },
    },
  };
  </script>
  
  <style scoped>
  /* Full-page container */
  .signup-page {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f5f5f5;
    margin: 0;
    padding: 0;
  }
  
  /* Signup Form Container */
  .signup-container {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 300px;
    text-align: center;
  }
  
  /* Form Fields */
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 14px;
  }
  
  input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  /* Button */
  .btn {
    padding: 10px 20px;
    background-color: #1976d2;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    width: 100%;
    font-size: 16px;
  }
  
  .btn:hover {
    background-color: #155a9e;
  }
  
  /* Messages */
  .success {
    color: green;
    margin-top: 10px;
  }
  
  .error {
    color: red;
    margin-top: 10px;
  }
  </style>
  