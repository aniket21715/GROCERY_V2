<template>
  <NavBar/>
    <div>
      <h2>Store Manager Registration</h2>
      <form @submit.prevent="StoreManagerRegister">
        <label for="username">Username:</label>
        <input type="text" v-model="username" required />
  
        <label for="password">Password:</label>
        <input type="password" v-model="password" required />
  
        <button type="submit">Register</button>
      </form>
    </div>
  </template>
  
  <script>
  import NavBar from '@/components/NavBar.vue';
  export default {
    name: 'StoreManagerLogin',
    components: {
    NavBar,
   },
    data() {
      return {
        username: '',
        password: '',
      };
    },
    methods: {
      async StoreManagerRegister() {
        try {
          const response = await fetch('http://localhost:5000/register/store-manager', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              username: this.username,
              password: this.password,
            }),
          });
  
          const data = await response.json();
  
          if (response.ok) {
            // Registration successful, you can handle the response accordingly
            console.log('Store Manager registered successfully', data);
          } else {
            // Handle registration errors
            console.error('Store Manager registration failed', data);
          }
        } catch (error) {
          console.error('An error occurred during registration', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add your styling here */
  </style>
  