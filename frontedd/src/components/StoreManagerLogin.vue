<template>
  <div>
    <NavBar />

    <div class="container mt-5">
      <div class="card mx-auto" style="max-width: 400px;">
        <div class="card-body">
          <h2 class="text-center mb-4">Store Manager Login</h2>

          <form @submit.prevent="login">
            <div class="mb-3">
              <label for="username" class="form-label">Username:</label>
              <input type="text" v-model="smdata.username" class="form-control" required>
            </div>

            <div class="mb-3">
              <label for="password" class="form-label">Password:</label>
              <input type="password" v-model="smdata.password" class="form-control" required>
            </div>

            <div class="text-center">
              <button type="submit" class="btn btn-primary">Login</button>
            </div>
          </form>

          <div v-if="message" class="alert mt-3" :class="thismessagetype">
            {{ message }}
          </div>
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

  .alert {
    padding: 10px;
    border-radius: 5px;
    margin-top: 10px;
  }

  .alert-success {
    background-color: #d4edda;
    border-color: #c3e6cb;
    color: #155724;
  }

  .alert-danger {
    background-color: #f8d7da;
    border-color: #f5c6cb;
    color: #721c24;
  }
</style>


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
