<template>
  <footer class="bg-dark text-white py-3">
    <div class="container">
      <div class="row">
        <!-- About Us -->
        <div class="col-md-6">
          <h5 class="text-uppercase mb-3">About Us</h5>
          <p class="text-light">
            We're on a mission to redefine your grocery shopping experience. Explore top-notch products at your fingertips.
          </p>
        </div>

        <!-- Our Services -->
        <div class="col-md-6">
          <h5 class="text-uppercase mb-3">Our Services</h5>
          <p class="text-light">
            Seamless grocery shopping with our app. Browse, order, and enjoy doorstep delivery of quality products.
          </p>
        </div>
      </div>

      <!-- Copyright -->
      <div class="mt-3 text-light text-center">
        © 2023 Your Grocery App. All rights reserved.
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'FooTer',
};
</script>

<style scoped>
/* Custom Styles for a Cool Look */
footer {
  background-color: #635f5f; /* Dark Grey */
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  height: 2.8inch; /* Set your preferred height */
  border-radius: 1cm;
}

h5 {
  color: #25f97a; /* Material Yellow 800 */
}

.text-light {
  color: rgba(255, 255, 255, 0.692);
}

/* Feel free to add more styles as needed */
</style>
