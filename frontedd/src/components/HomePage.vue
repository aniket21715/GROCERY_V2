<template>
  <div>
    <NavBar />
    <SearchProduct @search="performSearch"/>

    <div class="container mt-4" style="background: linear-gradient(to right, #8ACA2B, #5CB85C);">
      <div class="card bg-light">
        <div class="card-header bg-primary text-white">
          <h2 class="text-center">Grocery Store</h2>
        </div>

        <div class="card-body">
          <p class="lead text-center">Welcome to the e-shop. Fulfill your needs with our quality products.</p>
        </div>

        <div class="card-body">
          <h3 class="card-title">Products</h3>

          <div v-if="products.length > 0">
            <div class="row">
              <div v-for="product in products" :key="product.id" class="col-md-4 mb-4">
                <div class="card">
                  <!-- Update the image source attribute to use an absolute path -->
                  <img :src="getImagePath(product)" alt="Product Image" class="card-img-top" style="height: 200px; object-fit: cover;">

                  <div class="card-body">
                    <h5 class="card-title">{{ product.name }}</h5>
                    <p class="card-text">{{ product.description }}</p>
                    <p class="card-text">Stock: {{ product.stock }}</p>
                    <p class="card-text">Price: ₹{{ product.price }}</p>
                    <p class="card-text">Category: {{ product.category.name }}</p>
                  </div>
                  <div class="input-group mb-3">
                    <span class="input-group-text">₹</span>
                    <span class="input-group-text">{{ product.price }}</span>
                    <input type="number" class="form-control" v-model="product.quantity" placeholder="Number of Items" name="count">
                    <input type="hidden" name="product" :value="product.id">
                    <button @click="addToCart(product)">Add to Cart</button>                 
                  </div>
                  <!-- Display success message only for the specific product -->
                  <div v-if="product.successMessage && product.successProductId === product.id" class="alert alert-success mt-3">
                    {{ product.successMessage }}
                  </div>

                </div>                
              </div>
            </div>
          </div>

          <div v-else>
            <p class="text-center">No products available.</p>
          </div>
        </div>
      </div>
    </div>
     <!-- Button to navigate to SubmitFeedback page -->
     <router-link to="/SubmitFeedback" class="btn btn-primary">Submit Feedback</router-link>

      <!-- Display feedback -->
      <!-- Display feedback in circular cards -->
      <div v-if="feedbackList.length > 0">
          <h3 class="mt-4 mb-3">Feedback</h3>
          <div v-for="(feedback, index) in feedbackList" :key="index" class="card mt-3" style="background-color: #ffdce5;">
            <div class="card-body">
              <p class="card-text">{{ feedback.content }}</p>
            </div>
          </div>
        </div>
        <div v-else>
          <p class="mt-4">No feedback available.</p>
        </div>
     
    <FooTer />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import FooTer from '@/components/FooTer.vue';
import SearchProduct from './SearchProduct.vue';
export default {
  name: 'HomePage',
  components: {
    NavBar,
    FooTer,
    SearchProduct,
  },
  data:() =>( {
      products: [],
      cart:[],
      successMessage: '',
      feedbackList: [],
  }),
  created() {
    this.fetchProducts();
    this.fetchFeedback();

  },
  methods: {
    async fetchProducts() {
    try {
      const response = await fetch('http://localhost:5000/get-products');
      if (response.ok) {
        const data = await response.json();
        const { products } = data; // Destructure the products array from the response
        this.products = products;
      } else {
        console.error("Failed to fetch", response.status);
      }
    } catch (error) {
      console.error("Error occurred", error);
    }
  },
    // Create a method to get the absolute path of the image
    getImagePath(product) {
  return `http://localhost:5000//${product.image}`;
},
addToCart(product) {
  const accessToken = localStorage.getItem('access_token');

  // Ensure quantity is a non-negative integer
  const quantity = Math.max(0, Math.floor(product.quantity));

  // Check if the requested quantity is greater than the available stock
  if (quantity > product.stock) {
    console.error(`Cannot add ${quantity} items to cart. Available stock is ${product.stock}.`);
    return; // Exit the function to prevent adding to cart
  }

  // Include the validated quantity in the request body
  const requestBody = {
    quantity,
  };

  // Make a request to add the product to the cart
  fetch(`http://localhost:5000/add-to-cart/${product.id}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
    },
    body: JSON.stringify(requestBody),
  })
    .then(response => {
      if (response.ok) {
        // Handle success
        console.log(`Added ${quantity} ${product.name}(s) to cart successfully`);
        product.successMessage = 'Product added successfully!';
        product.successProductId = product.id; // Set the success product ID
      } else {
        // Handle error
        console.error('Failed to add product to cart:', response.status);
        return response.json(); // Add this line to log the response body
      }
    })
    .then(data => {
      console.log('Server response:', data); // Log the response body
    })
    .catch(error => {
      console.error('Error adding product to cart:', error);
    });
},


performSearch(query) {
    // Implement your search logic here
    // For example, let's filter products based on the name
    if (query.trim() === '') {
      // If the search query is empty, show all products
      this.fetchProducts(); // Refresh the products list to show all products
    } else {
      this.products = this.products.filter(product =>
        product.name.toLowerCase().includes(query.toLowerCase())||
        product.category.name.toLowerCase().includes(query.toLowerCase())
      );
    }
  },

  async fetchFeedback() {
      try {
        const response = await fetch('http://localhost:5000/get-feedback');
        if (response.ok) {
          const data = await response.json();
          this.feedbackList = data.feedback_list;
        } else {
          console.error('Failed to fetch feedback', response.status);
        }
      } catch (error) {
        console.error('Error occurred while fetching feedback', error);
      }
    },
  },

}

</script>
  
<style scoped>
  /* Add your styling here */

  body {
    background-color: #91e7df;
    background: linear-gradient(to right, #a7ec41, #67d767);
  }

  

  .card {
    border: 2px solid #252a30;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(158, 138, 138, 0.1);
    margin-top: 10px;
  }

  .card-header {
    background-color: #cca1d3;
    color: rgb(192, 214, 67);
    text-align: center;
    
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
  }

  .lead {
    color: #06213c;
    font-size: 1.2em; /* Adjust the font size as needed */
    font-weight: bold; /* Make the text bold */
  }

  .card-title {
    color: #541818;
  }

  .card-text {
    color: #3a6c97;
    box-sizing: 100px;
  }

  img.card-img-top {
    border-bottom: 1px solid #c1d7ec;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
  }

  .btn-primary {
    background-color: #3792f4;
    border-color: #17c514;
  }

  .btn-primary:hover {
    background-color: #0056b3;
    border-color: #0056b3;
  }

  .footer {
    background-color: #343a40;
    color: white;
    padding: 10px 0;
    text-align: center;
    position: fixed;
    width: 100%;
    bottom: 0;
  }
</style>
