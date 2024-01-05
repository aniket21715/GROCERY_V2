<template>
  <div>
    <NavBar />
    
    <div class="container d-flex justify-content-center align-items-center min-vh-100">
      <div class="card w-50">
        <div class="card-body">
          <h2 class="card-title text-center mb-4">Register</h2>
          
          <form @submit.prevent="register">
            <div class="mb-3">
              <label for="username" class="form-label">Username:</label>
              <input v-model="username" type="text" id="username" class="form-control" required>
            </div>
            
            <div class="mb-3">
              <label for="password" class="form-label">Password:</label>
              <input v-model="password" type="password" id="password" class="form-control" required>
            </div>
            
            <div class="d-grid gap-2">
              <button type="submit" class="btn btn-primary btn-block">Register</button>
            </div>
          </form>
          
          <div class="text-center mt-3">
            <p>
              Already have an account? 
              <router-link to="/LoginUser" class="link-primary">Login Now</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>

<script>
import NavBar from '@/components/NavBar.vue';
  
export default {
  name: 'RegisterUser',
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
    async register() {
      try {
        // Send registration request to the Flask backend using fetch
        const response = await fetch('http://localhost:5000/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        });

        // Parse the JSON response
        const data = await response.json();

        // Check if registration was successful
        if (response.ok) {
          console.log('Registration successful!');
          // Optionally, you can perform additional actions on successful registration
          this.$router.push('/LoginUser');
        } else {
          console.error('Registration failed:', data.message);
          // Handle failed registration, show error message, etc.
        }
      } catch (error) {
        console.error('An error occurred during registration:', error.message);
        // Handle other errors (e.g., network issues)
      }
    }
  }
};
</script>
