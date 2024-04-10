<template>
  <NavBar />
  <div class="container d-flex align-items-center justify-content-center min-vh-100">
    <div class="card p-4" style="width: 500px; background-color: #f8f9fa; border: 2px solid #17a2b8;">
      <h2 class="text-center mb-4" style="color: #17a2b8;">Your Cart</h2>

      <div v-if="cart.length > 0">
        <table class="table">
          <thead>
            <tr>
              <th scope="col">Product Image</th>
              <th scope="col">Product Name</th>
              <th scope="col">Quantity</th>
              <th scope="col">Price</th>
              <th scope="col">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in cart" :key="item.id" class="cart-item">
              <td>
                <img
                  :src="getImagePath(item.product)"
                  alt="Product Image"
                  class="img-fluid"
                  style="max-height: 100px; object-fit: cover;"
                />
              </td>
              <td>{{ item.product ? item.product.name : 'Product Name Not Available' }}</td>
              <td>{{ item.quantity }}</td>
              <td>₹{{ item.product ? item.product.price : 'Price Not Available' }}</td>
              <td>
                <button @click="removeFromCart(item.product.id)" class="btn btn-danger">Remove</button>
              </td>
            </tr>
          </tbody>
        </table>

        <div class="total-amount">
          <p style="color: #17a2b8;">Total Amount to be Paid: ₹{{ totalAmount }}</p>
          <button @click="checkout" class="btn btn-primary">Checkout</button>

          <!-- Display success message only if purchase is successful -->
          <div v-if="purchaseSuccess" class="alert alert-success mt-3" style="background-color: #28a745; color: #fff;">
            {{ successMessage }}
          </div>
        </div>
      </div>

      <div v-else>
        <!-- Display this message only if the cart is empty -->
        <p class="text-center">Your cart is empty.</p>
      </div>
    </div>
  </div>
</template>

<!-- Add your existing script and style sections here -->


<script>
import NavBar from '@/components/NavBar.vue';
export default {
  name:'CartPage',
  components: {
    NavBar,
  },
  data() {
    return {
      cart: [],
      access_token:null, 
      purchaseSuccess: false,
      successMessage: '',
      // The array to store cart items
    };
  },
  created() {
    // Fetch the user's cart when the component is created
    this.fetchCart();
  },
  computed: {
    totalAmount() {
      // Calculate the total amount based on the items in the cart
      return this.cart.reduce((total, item) => {
        // Ensure that the item and product exist before calculating
        if (item && item.product) {
          total += item.quantity * item.product.price;
        }
        return total;
      }, 0);
    },
  },
  methods: {
    fetchCart() {
  const accessToken = localStorage.getItem('access_token');

  // Make a request to fetch the user's cart data
  fetch('http://localhost:5000/get-cart', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
    },
  })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error(`Failed to fetch cart: ${response.status}`);
      }
    })
    .then(data => {
      // Update the local cart array with the fetched data
      this.cart = data.cart;
    })
    .catch(error => {
      console.error('Error fetching cart:', error);
    });
},
removeFromCart(cartItemId) {
  // Use this.access_token to access the access_token from data
  const access_token = localStorage.getItem('access_token');

  // Make a request to remove the item from the cart
  fetch(`http://localhost:5000/remove-from-cart/${cartItemId}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${access_token}`, // Include the user's authentication token
    },
  })
    .then(response => {
      if (response.ok) {
        // If the removal is successful, update the local cart array
        this.cart = this.cart.filter(item => item.product.id !== cartItemId);
      } else if (response.status === 404) {
        // Handle the case where the item is not found in the cart
        console.warn('Item not found in cart. It may have already been removed.');
      } else {
        console.error('Failed to remove item from cart:', response.status);
      }
    })
    .catch(error => {
      console.error('Error removing item from cart:', error);
    });
},

getImagePath(product) {
    return product && product.image ? `http://localhost:5000/uploads/${product.image}` : 'path_to_default_image';
  },

  checkout() {
      const access_token = localStorage.getItem('access_token');
      fetch('http://localhost:5000/checkout', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${access_token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ cart: this.cart }),
      })
        .then(response => {
          if (response.ok) {
            this.cart = [];
            this.purchaseSuccess = true;
            this.successMessage = 'Purchase successful!';
          } else {
            console.error('Failed to checkout:', response.status);
            this.purchaseSuccess = false;
            this.successMessage = 'An error occurred during purchase. Please try again.';
          }
        })
        .catch(error => {
          console.error('Error during checkout:', error);
          this.purchaseSuccess = false;
          this.successMessage = 'An error occurred during purchase. Please try again.';
        });
    },

  },
};
</script>
