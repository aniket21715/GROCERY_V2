<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <router-link to="/" class="navbar-brand">GroceryApp</router-link>
    
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ml-auto">
        <li class="nav-item">
          <router-link to="/" class="nav-link">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/LoginUser" class="nav-link">Login</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/RegisterUser" class="nav-link">Register</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/AdminLogin" class="nav-link">Admin</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/AdminUserLogout" class="nav-link">Logout</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/StoreManagerRegister" class="nav-link">Managersignup</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/StoreManagerLogin" class="nav-link">ManagerLogin</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/StoreManagerLogout" class="nav-link">ManagerLogout</router-link>
        </li>

      </ul>
    </div>
  </nav>
</template>

  
  
  <script>
  export default {
    name: 'NavBar',
  };
  </script>
  
  