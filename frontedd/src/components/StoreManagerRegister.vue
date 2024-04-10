<template>
  <div>
    <NavBar/>
    
    <div class="container mt-5">
      <div class="card mx-auto" style="max-width: 400px;">
        <div class="card-body">
          <h2 class="text-center mb-4">Store Manager Registration</h2>

          <form @submit.prevent="StoreManagerRegister">
            <div class="mb-3">
              <label for="username" class="form-label">Username:</label>
              <input type="text" v-model="username" class="form-control" required />
            </div>

            <div class="mb-3">
              <label for="password" class="form-label">Password:</label>
              <input type="password" v-model="password" class="form-control" required />
            </div>

            <div class="text-center">
              <button type="submit" class="btn btn-primary">Register</button>
            </div>
            <div class="text-center mt-3">
            <p>
              Already have an account? 
              <router-link to="/StoreManagerLogin" class="link-primary">Login Now</router-link>
            </p>
          </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
  /* Add your styling here */

  .btn-primary {
    background-color: #007bff;
    border-color: #007bff;
  }

  .btn-primary:hover {
    background-color: #0056b3;
    border-color: #0056b3;
  }
</style>

  <script>
  import NavBar from '@/components/NavBar.vue';
  export default {
    name: 'StoreManagerRegister',
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
            this.$router.push('/StoreManagerLogin');

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
  