<template>
    <div class="homepage">
      <!-- Navigation Bar (Dashboard) -->
      <nav class="navbar">
        <div class="navbar-left">
          <button class="btn btn-primary" @click="goToLogin">Login</button>
          <button class="btn btn-secondary" @click="goToSignup">Sign Up</button>
        </div>
        <div class="navbar-right">
          <button class="btn btn-link" @click="goToAboutUs">About Us</button>
          <button class="btn btn-link" @click="goToContactUs">Contact Us</button>
        </div>
      </nav>
  
      <!-- Main Content -->
      <div class="content">
        <h1>Welcome to AI Personal Financial Advisor</h1>
        <p>Take control of your finances with smart insights and recommendations.</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "HomePage",
    methods: {
      goToLogin() {
        this.$router.push("/login");
      },
      goToSignup() {
        this.$router.push("/signup");
      },
      goToAboutUs() {
        this.$router.push("/about-us");
      },
      goToContactUs() {
        this.$router.push("/contact-us");
      },
    },
  };
  </script>
  
  <style scoped>
  /* Full-page container styles */
  .homepage {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    height: 100vh; /* Full height of the viewport */
    width: 100vh; /* Full width of the viewport */
    background-color: #f5f5f5; /* Light gray background */
  }
  
  /* Navigation Bar Styles */
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%; /* Full width */
    padding: 10px 20px;
    background-color: #1976d2; /* Blue background */
    color: white;
  }
  
  .navbar-left,
  .navbar-right {
    display: flex;
    gap: 10px; /* Space between buttons */
  }
  
  /* Button Styles */
  .btn {
    padding: 8px 16px;
    font-size: 14px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn-primary {
    background-color: #4caf50; /* Green background */
    color: white;
  }
  
  .btn-secondary {
    background-color: #f44336; /* Red background */
    color: white;
  }
  
  .btn-link {
    background: none;
    border: none;
    color: white;
    text-decoration: underline;
    cursor: pointer;
  }
  
  /* Main Content Styles */
  .content {
    flex: 1; /* Take up remaining space */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 20px;
  }
  
  .content h1 {
    font-size: 3rem; /* Large heading */
    margin-bottom: 20px;
    color: #333;
  }
  
  .content p {
    font-size: 1.2rem;
    color: #555;
  }
  </style>
  