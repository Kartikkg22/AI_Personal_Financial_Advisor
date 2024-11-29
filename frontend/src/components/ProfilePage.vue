<template>
  <div class="profile-page">
    <header>
      <h1>Your Profile</h1>
    </header>

    <section v-if="user">
      <h2>Profile Details</h2>
      <p><strong>Name:</strong> {{ user.name }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>Income:</strong> ${{ user.income }}</p>
      <p><strong>Expenses:</strong> ${{ user.expenses }}</p>
      <p><strong>Savings:</strong> ${{ user.savings }}</p>
    </section>

    <section v-else>
      <p>Loading your profile...</p>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ProfilePage",
  data() {
    return {
      user: null, // To store user profile data
    };
  },
  mounted() {
    this.fetchUserProfile();
  },
  methods: {
    async fetchUserProfile() {
      const userId = localStorage.getItem("userId");
      if (!userId) {
        console.error("No user ID found in localStorage. Redirecting to login.");
        this.$router.push("/login"); // Redirect to login if not authenticated
        return;
      }

      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/user/${userId}`);
        this.user = response.data;
      } catch (error) {
        console.error("Error fetching user profile:", error);
        if (error.response && error.response.status === 404) {
          alert("User not found. Please log in again.");
          localStorage.removeItem("isAuthenticated");
          localStorage.removeItem("userId");
          this.$router.push("/login");
        }
      }
    },
  },
};
</script>

<style scoped>
.profile-page {
  text-align: center;
  margin: 20px;
}

header {
  background-color: #1976d2;
  color: white;
  padding: 20px;
  border-radius: 8px;
}

section {
  margin-top: 20px;
}
</style>
