<template>
    <div>
      <!-- Your existing components and HTML -->
  
      <button @click="logout">Logout</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'StoreManagerLogout',
    
    methods: {
      async logout() {
        try {
          const response = await fetch('http://localhost:5000/store-manager/logout', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          });
  
          if (response.ok) {
            console.log('Logout successful');
            // Clear the access token from local storage or any other cleanup
            localStorage.removeItem('access_token');
            // Redirect to the login page or any other desired action
            this.$router.push('/StoreManagerLogin');
          } else {
            console.log('Logout failed:', response.status);
            // Handle logout failure, if needed
          }
        } catch (error) {
          console.error('Error:', error);
          // Handle any network or unexpected errors
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add your component-specific styles here */
  </style>
  