<template>
  <div>
    <NavBar />
    <div>
      <h2>Store Manager Login</h2>
      <form @submit.prevent="login">
        <label for="username">Username:</label>
        <input type="text" v-model="smdata.username" required>
        <label for="password">Password:</label>
        <input type="password" v-model="smdata.password" required>
        <button type="submit">Login</button>
      </form>
      <div v-if="message" class="alert" :class="thismessagetype">
        {{ message }}
      </div>
    </div>
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
      smdata: {
        username: '',
        password: '',
      },
      message: '',
      thismessagetype: '',
    };
  },
  methods: {
    async login() {
  try {
    const response = await fetch('http://localhost:5000/store-manager/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(this.smdata),
    });

    const data = await response.json();
    console.log('Response:', response);
    console.log('Data:', data);

    if (response.ok) {
      if (data.status === 'approved') {
        console.log('Redirecting to dashboard');
        localStorage.setItem('access_token', data.access_token);
        this.message = 'Login successful';
        this.thismessagetype = 'alert-success';
        this.$router.push('/StoreManagerDashboard');
      } else {
        console.log('Store manager not approved. Please wait for approval.');
        this.message = 'Store manager not approved. Please wait for approval.';
        this.thismessagetype = 'alert-danger';
      }
    } else {
      console.log('Error response:', data.message);
      this.message = 'Invalid credentials or store manager not approved';
      this.thismessagetype = 'alert-danger';
    }
  } catch (error) {
    console.error('Error:', error);
    this.message = 'An error occurred during login';
    this.thismessagetype = 'alert-danger';
  }
},
  },
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
