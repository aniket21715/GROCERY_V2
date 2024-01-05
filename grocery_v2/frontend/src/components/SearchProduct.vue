<!-- SearchBar.vue -->
<template>
    <form class="classic-search-form" role="search">
      <input v-model="searchQuery" @input="searchProducts" class="form-control classic-search-input" type="search" placeholder="🌶️ Search your items" aria-label="Search">
      <button class="btn btn-outline-danger classic-search-button" type="submit">Search</button>
    </form>
  </template>
  
  <style scoped>
  /* Redesigned styling for a spicy and medium-sized look */
  .classic-search-form {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px; /* Add padding for space */
  }
  
  /* Style the input for emphasis */
  .classic-search-input {
    font-weight: bold;
    border: 2px solid #ff5722; /* Spicy orange border */
    border-radius: 15px;
    padding: 8px; /* Adjust padding for a medium-sized input */
    margin-right: 10px;
  }
  
  /* Style the search button */
  .classic-search-button {
    font-weight: bold;
    border: 2px solid #ff5722; /* Spicy orange border */
    border-radius: 15px;
    padding: 8px; /* Adjust padding for a medium-sized button */
  }
  
  /* You can add more styling based on your preferences */
  </style>
  
  <script>
  export default {
    name:'SearchProduct',
    data() {
      return {
        searchQuery: '',
      };
    },
    methods: {
      searchProducts() {
        // You can perform the search logic here
        // You might want to update the list of products based on the search query
        // For simplicity, let's just emit an event for the parent component to handle
        this.$emit('search', this.searchQuery);
      },
    },
  };
  </script>
  
 