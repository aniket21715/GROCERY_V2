<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <router-link to="/" class="navbar-brand">GroceryApp</router-link>

      <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent" >
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <router-link to="/" class="nav-link">Home</router-link>
          </li>

          <div class="collapse navbar-collapse" id="navbarNavLightDropdown">
            <ul class="navbar-nav">
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDarkDropdownMenuLink" role="button"
                  data-bs-toggle="dropdown" aria-expanded="false">
                  User
                </a>
                <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="navbarDarkDropdownMenuLink">
                  <li class="nav-item">
                    <router-link to="/LoginUser" class="nav-link">Login</router-link>
                  </li>
                  <li class="nav-item">
                    <router-link to="/RegisterUser" class="nav-link">Register</router-link>
                  </li>
                  <li class="nav-item">
                    <router-link to="/UserProfile" class="nav-link">Profile</router-link>
                  </li>
                  <li class="nav-item">
                    <router-link to="/PurchaseHistory" class="nav-link">OrderHistory</router-link>
                  </li>
                </ul>
              </li>
            </ul>
          </div>
          <li class="nav-item">
            <router-link to="/AdminLogin" class="nav-link">Admin</router-link>
          </li>
          <div class="collapse navbar-collapse" id="navbarNavLightDropdown">
            <ul class="navbar-nav">
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDarkDropdownMenuLink" role="button"
                  data-bs-toggle="dropdown" aria-expanded="false">
                  Manager
                </a>
                <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="navbarDarkDropdownMenuLink">
                  <li class="nav-item">
                    <router-link to="/StoreManagerRegister" class="nav-link">Manager Signup</router-link>
                  </li>
                  <li class="nav-item">
                    <router-link to="/StoreManagerLogin" class="nav-link">Manager Login</router-link>
                  </li>
                </ul>
              </li>
            </ul>
          </div>
          
          <li class="nav-item">
            <router-link to="/CartPage" class="nav-link">
              <img src="../assets/cart.png" alt="Logo" class="cart-icon" style="width: 24px; height: 24px;" /> Cart
            </router-link>
          </li>

          <li class="nav-item">
            <button @click="logout" class="btn btn-outline-danger my-2 my-sm-0">Logout</button>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</template>

<style scoped>
/* Add your styling here */
/* Custom styling for the collapsed navbar */
@media (max-width: 768px) {
  .navbar-toggler-icon {
    background-color: #ff5722; /* Spicy orange color for the toggler icon */
  }

  .navbar-toggler {
    border-color: #ff5722; /* Spicy orange color for the toggler button border */
  }

  .navbar-nav {
    background-color: rgb(106, 124, 141); /* Dark background color for the collapsed navbar items */
    border-top: 1px solid #325f8d; /* Light border at the top of the collapsed navbar */
    text-align: center; /* Center-align the collapsed navbar items */
    width: 100%; /* Full width for collapsed navbar items */
    position: absolute;
    top: 56px; /* Adjust the top position based on your navbar height */
  }

  .navbar-nav .nav-item {
    margin: 0; /* Remove default margin */
    width: 100%; /* Full width for each collapsed navbar item */
  }

  .navbar-nav .nav-link {
    color: #e9db15; /* White text color for collapsed navbar links */
  }
}
.navbar-light {
  background-color: #ba49b5;
  /* Light gray background */
}

.navbar-brand {
  font-weight: bold;
  color: #0aab30;
  /* Green color */
}

.navbar-nav .nav-link {
  color: #007bff;
  /* Blue color for links */
}

.btn-outline-danger {
  color: #dc3545;
  /* Red color for logout button */
  border-color: #dc3545;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  color: rgb(209, 118, 118);
}
</style>


  
<script>

export default {
  name: 'NavBar',
  methods: {
    async logout() {
      try {
        // You may want to send a request to the server to invalidate the token,
        // but for simplicity, let's just remove the token from localStorage.
        localStorage.removeItem("access_token");

        // Redirect to the login page (adjust the route as needed)
        this.$router.push('/');

        console.log('Logout successful!');
      } catch (error) {
        console.error('An error occurred during admin logout:', error.message);
        // Handle other errors if necessary
      }
    }
  },
};
</script>
  
  