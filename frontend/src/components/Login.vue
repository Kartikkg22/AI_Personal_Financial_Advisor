<template>
    <div class="login-page">
      <div class="login-container">
        <h1>Login</h1>
        <form @submit.prevent="handleLogin">
          <!-- Username Field -->
          <div class="form-group">
            <label for="username">Username</label>
            <input
              type="text"
              id="username"
              v-model="username"
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
  
          <!-- Submit Button -->
          <button type="submit" class="btn">Login</button>
        </form>
  
        <!-- Error Message -->
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "LoginPage",
    data() {
      return {
        username: "",
        password: "",
        errorMessage: null,
      };
    },
    methods: {
      async handleLogin() {
        try {
          // Make an API call to the backend for authentication
          const response = await axios.post("http://127.0.0.1:5000/api/login", {
            username: this.username,
            password: this.password,
          });
  
          // If login is successful, save the state in localStorage and redirect
          if (response.status === 200) {
            console.log("Login successful:", response.data);
  
            // Save authentication status in localStorage
            const user = response.data.user;
            localStorage.setItem("isAuthenticated", "true");
            localStorage.setItem("userId", user.id);
            localStorage.setItem("userName", user.name);
            localStorage.setItem("userEmail", user.email);
  
            // Redirect to the homepage
            this.$router.push("/home-page");
          }
        } catch (error) {
          // Handle login errors
          if (error.response && error.response.data) {
            this.errorMessage = error.response.data.error;
          } else {
            this.errorMessage = "An unexpected error occurred. Please try again.";
          }
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Full-page container */
  .login-page {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f5f5f5;
    margin: 0;
    padding: 0;
  }
  
  /* Login Form Container */
  .login-container {
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
  
  /* Error Message */
  .error {
    color: red;
    margin-top: 10px;
    font-size: 14px;
  }
  </style>
  