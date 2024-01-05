<template>
    <div>
      <!-- Your existing components and HTML -->
  
      <button @click="logout">Logout</button>
    </div>
  </template>
  
  <script>
  export default {
    name:'AdminUserLogout',
    methods: {
      async logout() {
        try {
          const accessToken = localStorage.getItem('Token');
  
          if (!accessToken) {
            console.error('Access token not found. User may not be authenticated.');
            // Optionally, you can redirect the user to the login page or handle it as needed
            this.$router.push('/user-login');
            return;
          }
  
          const response = await fetch('http://localhost:5000/user/logout', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${accessToken}`,
            },
            body: JSON.stringify({}), // Empty JSON payload
          });
  
          console.log('Logout Response:', response);
  
          if (response.ok) {
            console.log('Logout successful');
            // Clear the access token from local storage or any other cleanup
            localStorage.removeItem('access_token');
            // Redirect to the login page or any other desired action
            this.$router.push('/');
          } else {
            console.error('Logout failed:', response.status, await response.json());
            // Handle logout failure, if needed
          }
        } catch (error) {
          console.error('Error during logout:', error);
          // Handle any network or unexpected errors
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add your component-specific styles here */
  </style>
  