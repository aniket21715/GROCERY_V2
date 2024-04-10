<template>
    <div>
      <NavBar />
      <div class="user-profile-card">
        <h2>User Profile</h2>
  
        <!-- User Details -->
        <div class="user-details-card">
          <p><strong>Username:</strong> {{ user.username }}</p>
          <p><strong>Email:</strong> {{ user.email }}</p>
          <p><strong>Password:</strong> *********</p> <!-- Display password securely -->
        </div>
  
        <!-- Edit Profile Form -->
        <div class="edit-profile-card">
          <h3>Edit Profile</h3>
          <form @submit.prevent="editProfile">
            <label for="username">Username:</label>
            <input v-model="editedUser.username" type="text" required>
  
            <label for="email">Email:</label>
            <input v-model="editedUser.email" type="email" required>
  
            <label for="password">New Password:</label>
            <input v-model="editedUser.password" type="password">
  
            <button type="submit">Save Changes</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import NavBar from '@/components/NavBar.vue';
  
  export default {
    name: 'UserProfile',
    components: {
      NavBar,
    },
    data() {
      return {
        user: {}, // User details fetched from the backend
        editedUser: {
          username: '',
          email: '',
          password: '',
        },
      };
    },
    mounted() {
      // Fetch user details when the component is mounted
      this.fetchUserDetails();
    },
  
    methods: {
      async fetchUserDetails() {
        try {
          const response = await fetch('http://localhost:5000/get-user-details', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
          });
  
          if (response.ok) {
            const data = await response.json();
            this.user = data.user;
          } else {
            console.error('Failed to fetch user details:', response.status);
          }
        } catch (error) {
          console.error('Error fetching user details:', error);
        }
      },
      async editProfile() {
        try {
          const response = await fetch('http://localhost:5000/edit-user-details', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
            body: JSON.stringify(this.editedUser),
          });
  
          if (response.ok) {
            // Handle success
            console.log('User details updated successfully');
            window.location.reload();
          } else {
            console.error('Failed to update user details:', response.status);
          }
        } catch (error) {
          console.error('Error updating user details:', error);
        }
      },
    },
  };
  </script>
  
<style scoped>
.user-profile-card {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background: linear-gradient(to right, #c5654d, #e98f4a);
  color: #fff;
}

.user-details-card,
.edit-profile-card {
  margin-bottom: 20px;
}

.edit-profile-card form {
  display: flex;
  flex-direction: column;
}

.edit-profile-card label {
  margin-bottom: 8px;
  color: #fff;
}

.edit-profile-card input {
  padding: 8px;
  margin-bottom: 12px;
  border: 1px solid #fff;
  border-radius: 4px;
}

.edit-profile-card button {
  padding: 10px;
  background-color: rgb(201, 226, 120);
  color: #94113a;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>