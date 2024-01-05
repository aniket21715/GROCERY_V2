<template>
  <NavBar/>
    <div>
      <h2>Store Manager Dashboard</h2>
      <!-- Add your dashboard components/content here -->
    </div>
  </template>
  
  <script>
  import NavBar from './NavBar.vue';
  export default {
    name: 'StoreManagerDashboard',
    components:{
      NavBar,
    }
  };
  </script>
  