<template>
    <NavBar />
      <div class="card">
        <div class="card-body">
          <h2 class="text-center mb-4">Home Page</h2>
          <p class="text-center">Welcome to the home page! Customize this content based on your application's needs.</p>         
        </div>
      </div>
    <FooTer />
  </template>
  
  <style scoped>
    /* Add your styling here */
  </style>
  
  <script>
  import NavBar from '@/components/NavBar.vue';
  import FooTer  from '@/components/FooTer.vue';

export default {
  name: 'HomePage',
  components: {
    NavBar,
    FooTer,
  },
};
  </script>
  