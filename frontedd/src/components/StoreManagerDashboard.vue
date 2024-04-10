<template>
  <div>
    <NavBar />

    <div class="container mt-4">
      <h2 class="text-center mb-4">Store Manager Dashboard</h2>

      <!-- Product Stocks Chart -->
      <div class="card mb-4">
        <div class="card-body">
          <h3 class="mb-3">Product Stocks</h3>
          <canvas id="productStockChart" width="200" height="100"></canvas>
        </div>
      </div>

      <!-- Add Product Button -->
      <div class="card mb-4">
        <div class="card-body">
          <button @click="goToAddProduct" class="btn btn-primary">Add Product</button>
        </div>
      </div>

      <!-- Products Section -->
      <h3 class="mb-3">Products</h3>

      <div v-if="products.length > 0">
        <div class="row">
          <div v-for="product in products" :key="product.id" class="col-md-4 mb-4">
            <div class="card">
              <img :src="getImagePath(product)" alt="Product Image" class="card-img-top" style="height: 200px; object-fit: cover;">

              <div class="card-body">
                <h5 class="card-title">{{ product.name }}</h5>
                <p class="card-text">{{ product.description }}</p>
                <p class="card-text">Stock: {{ product.stock }}</p>
                <p class="card-text">Price: ${{ product.price }}</p>
                <p class="card-text">Category: {{ product.category.name }}</p>

                <div class="d-flex justify-content-between">
                  <button @click="editProduct(product.id)" class="btn btn-info">Edit</button>
                  <button @click="deleteProduct(product.id)" class="btn btn-danger">Delete</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <p>No products available.</p>
      </div>

      <!-- Export CSV Button -->
      <button @click="exportProductsCSV" class="btn btn-success">Export Products as CSV</button>

      <!-- Add Category Request Form -->
      <div class="card mb-4">
        <div class="card-body">
          <h3 class="mb-3">Add Category Request</h3>
          <form @submit.prevent="sendCategoryRequest">
            <div class="form-group">
              <label for="categoryName">Category Name</label>
              <input type="text" v-model="categoryName" class="form-control" id="categoryName" required>
            </div>
            <div class="form-group">
              <label for="description">Description</label>
              <textarea v-model="description" class="form-control" id="description" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Submit Request</button>
          </form>
        </div>
      </div>

      <!-- Send Message Form -->
      <div class="card">
        <div class="card-body">
          <h2 class="card-title">Send Message to Admin</h2>
          <form @submit.prevent="sendMessage">
            <div class="mb-3">
              <label for="content" class="form-label">Message Content:</label>
              <textarea v-model="content" class="form-control" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Send Message</button>
          </form>
          <div v-if="successMessage" class="alert alert-success mt-3">
            {{ successMessage }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<!-- Your existing script and styles remain unchanged -->

<style scoped>
    #productStockChart {
    width: 70%;
    height: auto;
    border: 2px solid #4caf50; /* Green border for the chart */
    border-radius: 10px;
    font-weight: bold;
  }

  /* Button Styles */
  .btn-primary {
    background-color: #4c65af; /* Green */
    border-color: #4caf50;
  }

  .btn-primary:hover {
    background-color: #4554a0;
    border-color: #45a049;
  }

  .btn-info {
    background-color: #c72579; /* Blue */
    border-color: #2196f3;
  }

  .btn-info:hover {
    background-color: #bc15ce;
    border-color: #1e87f0;
  }

  .btn-danger {
    background-color: #f44336; /* Red */
    border-color: #f44336;
  }

  .btn-danger:hover {
    background-color: #e53935;
    border-color: #e53935;
  }

  .btn-success {
    background-color: #d25b11; /* Orange */
    border-color: #ff9800;
  }

  .btn-success:hover {
    background-color: #dc700b;
    border-color: #f57c00;
  }

  /* Alert Styles */
  .alert-success {
    background-color: #a9f157; /* Light Green */
    color: #740707;
    border-color: #c34aab;
  }
</style>


<script>
import NavBar from '@/components/NavBar.vue';
import Chart from 'chart.js/auto';

export default {
  name: 'StoreManagerDashboard',
  components:{NavBar,},
  data:() =>( {
      products: [],
      categoryName: '',
      description: '',
      recipientId: '',
      content: '',
        }),
  created() {
    this.fetchProducts();
    this.fetchProductStocks();
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

    goToAddProduct() {
      // Redirect to AddCategory.vue
      this.$router.push('/AddProduct');
    },
    async editProduct(productId) {
  // Navigate to the edit product page with the product ID as a parameter
  this.$router.push(`/EditProduct/${productId}`);
},
async deleteProduct(productId) {
      // Confirm deletion with the user
      const confirmDelete = confirm('Are you sure you want to delete this product?');

      if (confirmDelete) {
        try {
          // Make a DELETE request to remove the product
          const response = await fetch(`http://localhost:5000/delete-product/${productId}`, {
            method: 'DELETE',
          });

          if (response.ok) {
            // If deletion is successful, update the products array
            this.products = this.products.filter(product => product.id !== productId);
            console.log('Product deleted successfully!');
          } else {
            console.error('Failed to delete product', response.status);
          }
        } catch (error) {
          console.error('Error occurred while deleting product', error);
        }
      }
    },
    async sendCategoryRequest() {
      try {
        const formdata =new FormData();
        formdata.append('category_name', this.categoryName)
        formdata.append('description', this.description)
        const response = await fetch('http://localhost:5000/store-manager/request-category', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          },
          body: JSON.stringify({
            category_name: this.categoryName,
            description: this.description,
          }),
        });

        if (response.ok) {
          // Reset form fields after successful request
          this.categoryName = '';
          this.description = '';
          this.successMessage = 'Request sent successfully!';
          console.log('Category request sent successfully!');
        } else {
          console.error('Failed to send category request', response.status);
        }
      } catch (error) {
        console.error('Error occurred while sending category request', error);
      }
    },
    async exportProductsCSV() {
    try {
      const response = await fetch('http://localhost:5000/export-products-csv', {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        },
      });

      if (response.ok) {
        // Trigger a notification or alert to inform the user
        alert('CSV export complete!');

        // Optionally, you can provide a direct link to download the file
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'product_details.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      } else {
        console.error('Failed to export products as CSV', response.status);
      }
    } catch (error) {
      console.error('Error occurred while exporting products as CSV', error);
    }
  },
  async sendMessage() {
      try {
        const response = await fetch('http://localhost:5000/send-message', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'), // Assuming you handle authentication with JWT
          },
          body: JSON.stringify({
            // recipient_id: this.recipientId,
            content: this.content,
          }),
        });

        if (response.ok) {
          console.log('Message sent successfully!');
          this.successMessage = 'Message sent successfully!';
          this.content = '';
        } else {
          console.error('Failed to send message', response.status);
        }
      } catch (error) {
        console.error('Error sending message', error);
      }
    },

    async fetchProductStocks() {
  try {
    // Fetch product stocks data
    const response = await fetch('http://localhost:5000/get-products');
    if (response.ok) {
      const data = await response.json();
      const productStocks = data.products.map(product => ({
        name: product.name,
        stock: product.stock,
      }));

      // Render the product stocks chart
      this.renderStocksChart(productStocks);
    } else {
      console.error("Failed to fetch product stocks", response.status);
    }
  } catch (error) {
    console.error("Error occurred while fetching product stocks", error);
  }
},

renderStocksChart(productStocks) {
  const ctx = document.getElementById('productStockChart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: productStocks.map(product => product.name),
      datasets: [{
        label: 'Product Stocks',
        data: productStocks.map(product => product.stock),
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      }],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
},

  
  },
};
</script>


<!-- <style scoped>
  /* Add your styling here */

  .btn-primary {
    background-color: #007bff;
    border-color: #007bff;
  }

  .btn-primary:hover {
    background-color: #0056b3;
    border-color: #0056b3;
  }

  .btn-info {
    background-color: #17a2b8;
    border-color: #17a2b8;
  }

  .btn-info:hover {
    background-color: #117a8b;
    border-color: #117a8b;
  }

  .btn-danger {
    background-color: #dc3545;
    border-color: #dc3545;
  }

  .btn-danger:hover {
    background-color: #bd2130;
    border-color: #bd2130;
  }
</style> -->