<template>
  <div class="profile-page">
    <header>
      <h1>User Profile</h1>
      <p>Welcome to your profile page.</p>
    </header>

    <section v-if="profile">
      <h2>Profile Details</h2>
      <p><strong>Name:</strong> {{ profile.name }}</p>
      <p><strong>Email:</strong> {{ profile.email }}</p>
    </section>

    <section v-else>
      <p>Loading profile data...</p>
    </section>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ProfilePage',
  data() {
    return {
      profile: null, // Store profile data
    };
  },
  mounted() {
    // Fetch profile data from the backend
    axios
      .get('http://127.0.0.1:5000/api/profile') // Ensure the backend server is running
      .then(response => {
        console.log('profile data:',response.data)
        this.profile = response.data;
      })
      .catch(error => {
        console.error('Error fetching profile data:', error);
      });
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
