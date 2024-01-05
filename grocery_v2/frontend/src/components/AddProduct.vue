<template>
    <div>
      <h2 class="text-center mb-4">Add Product</h2>
  
      <div class="card mx-auto" style="max-width: 400px;">
        <div class="card-body">
          <form @submit.prevent="addProduct">
  
            <div class="mb-3">
              <label for="name" class="form-label">Product Name:</label>
              <input type="text" v-model="product.name" class="form-control" required>
            </div>
  
            <div class="mb-3">
              <label for="description" class="form-label">Description:</label>
              <textarea v-model="product.description" class="form-control" required></textarea>
            </div>
  
            <div class="mb-3">
              <label for="stock" class="form-label">Stock:</label>
              <input type="number" v-model="product.stock" class="form-control" required>
            </div>
  
            <div class="mb-3">
              <label for="price" class="form-label">Price:</label>
              <input type="number" v-model="product.price" class="form-control" required>
            </div>
  
            <div class="mb-3">
              <label for="category" class="form-label">Category:</label>
              <select v-model="product.categoryId" class="form-select" required>
                <option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
            </div>
  
            <div class="mb-3">
              <label for="image" class="form-label">Image:</label>
              <input type="file" accept="image/*" @change="handleImageUpload" class="form-control" required>
            </div>
  
            <div class="text-center">
              <button type="submit" class="btn btn-primary">Add Product</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
<style scoped>
    /* Add your styling here */
  
    .btn-primary {
      background-color: #007bff;
      border-color: #007bff;
    }
  
    .btn-primary:hover {
      background-color: #0056b3;
      border-color: #0056b3;
    }
  </style>
  
<script>
export default {
    name: 'AddProduct',
    data() {
        return {
            product: {
                name: '',
                description: '',
                stock: 0,
                price: 0,
                categoryId: null,
                image: null,
            },
            categories: [],
        };
    },
    created() {
        this.fetchCategories();
    },
    methods: {
        fetchCategories() {
            // Fetch categories from the backend
            fetch('http://localhost:5000/get-categories')
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    this.categories = data.categories;
                })
                .catch(error => console.error('Error:', error));
        },
        handleImageUpload(event) {
            this.product.image = event.target.files[0];
        },
        async addProduct() {
            try {
                const formData = new FormData();
                formData.append('name', this.product.name);
                formData.append('description', this.product.description);
                formData.append('stock', this.product.stock);
                formData.append('price', this.product.price);
                formData.append('category_id', this.product.categoryId);
                if (this.product.image) {
                    formData.append('image', this.product.image, this.product.image.name);
                }

                const response = await fetch('http://localhost:5000/add-product', {
                    method: 'POST',
                    body: formData,
                });

                if (response.ok) {
                    console.log('Product added');
                    this.$router.push('/StoreManagerDashboard');
                } else {
                    console.log('Product not added. Server responded with:', response.status, response.statusText);
                    const errorData = await response.json();
                    console.log('Error data:', errorData);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        },
    },
};
</script>
  