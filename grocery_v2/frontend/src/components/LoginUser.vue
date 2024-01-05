<template>
  <div>
    <NavBar />
    
    <div class="container d-flex justify-content-center align-items-center min-vh-100">
      <div class="card w-75">
        <div class="card-body">
          <h2 class="card-title text-center mb-4">Login</h2>
          <form @submit.prevent="login">
            <div class="mb-3">
              <label for="username" class="form-label">Username:</label>
              <input v-model="username" type="text" id="username" class="form-control" required>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password:</label>
              <input v-model="password" type="password" id="password" class="form-control" required>
            </div>
            <div class="d-grid gap-2">
              <button type="submit" class="btn btn-primary btn-block">Login</button>
            </div>
          </form>
          
          <div class="text-center mt-3">
            <p>
              Don't have an account? 
              <router-link to="/RegisterUser" class="link-primary">Register</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped >

 
</style>
<script>
import jwt_decode from 'jwt-decode';
import NavBar from '@/components/NavBar.vue';
export default {
  name: 'LoginUser',
  components: {
    NavBar,
  },
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
  try {
    // Send login request to the Flask backend using fetch
    const response = await fetch('http://localhost:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: this.username,
        password: this.password,
      }),
    });

    // Check if login was successful
    if (response.ok) {
      const data = await response.json(); // Move this line here
      console.log('Login successful!');
      this.$router.push('/');
      var tokendecode = jwt_decode(data.access_token);
      localStorage.setItem("TOKEN", data.access_token);
      console.log(tokendecode);
      // Optionally, you can perform additional actions on successful login
    } else {
      const data = await response.json();
      throw new Error(data.message);
      // Handle failed login, show error message, etc.
    }
  } catch (error) {
    console.error('An error occurred during login:', error.message);
    // Handle other errors (e.g., network issues)
  }
}

  }
};
</script>
 