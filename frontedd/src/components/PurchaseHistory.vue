<!-- PurchaseHistory.vue -->
<template>
    <NavBar/>
    <div class="container mt-4">
      <h2>Order History</h2>
      <div class="table-responsive">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th scope="col">Image</th>
              <th scope="col">Product Name</th>
              <th scope="col">Quantity</th>
              <th scope="col">Purchase Date Time</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="purchase in purchaseHistory" :key="purchase.product.id">
              <td>
                <img
                  :src="getImagePath(purchase.product)"
                  alt="Product Image"
                  class="img-thumbnail"
                  style="max-height: 75px; object-fit: cover;"
                />
              </td>
              <td>{{ purchase.product.name }}</td>
              <td>{{ purchase.quantity }}</td>
              <td>{{ formatDateTime(purchase.purchase_date) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import NavBar from './NavBar.vue';
  export default {
    name:'PurchaseHistory',
    components:{NavBar},
    data() {
      return {
        purchaseHistory: [], // Initialize with the data received from the backend
      };
    },
    mounted() {
      // Fetch purchase history from the backend when the component is mounted
      this.fetchPurchaseHistory();
    },
    methods: {
        async fetchPurchaseHistory() {
    try {
        const access_token = localStorage.getItem('access_token');
        // Make an API request to fetch purchase history from the backend
        const response = await fetch('http://localhost:5000/purchase-history', {
            headers: {
                Authorization: `Bearer ${access_token}`, // Add your JWT token
            },
        });

        if (response.ok) {
            const data = await response.json();
            // Ensure that the property name matches the backend response
            this.purchaseHistory = data.purchase_history;
        } else {
            console.error('Failed to fetch purchase history');
        }
    } catch (error) {
        console.error('Error fetching purchase history:', error);
    }
},

getImagePath(product) {
    return product && product.image ? `http://localhost:5000/uploads/${product.image}` : 'path_to_default_image';
  },
  formatDateTime(dateTimeString) {
  const optionsDate = { day: '2-digit', month: '2-digit', year: 'numeric' };
  const optionsTime = { hour: '2-digit', minute: '2-digit', second: '2-digit' };

  const dateTime = new Date(dateTimeString);

  const formattedDate = dateTime.toLocaleDateString('en-GB', optionsDate);
  const formattedTime = dateTime.toLocaleTimeString('en-US', optionsTime);

  return `${formattedDate} ${formattedTime}`;
},

  
    },
  };
  </script>
  
  <style scoped>
  /* Add your component styles here */
  </style>
  