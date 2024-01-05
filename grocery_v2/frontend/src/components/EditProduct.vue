<template>
  <NavBar/>
  <div>
    <h2 class="text-center mb-4">Product Edit</h2>

    <div v-if="products.length > 0">
      <div class="row">
        <div v-for="product in products" :key="product.id" class="col-md-6 mb-4">
          <div class="card">
            <img :src="getImagePath(product)" alt="Product Image" class="card-img-top" style="height: 150px; object-fit: cover;">

            <div class="card-body">
              <div v-if="!product.edit">
                <h5 class="card-title">{{ product.name }}</h5>
                <p class="card-text">{{ product.description }}</p>
                <p class="card-text">Category: {{ product.category.name }}</p>
                <p class="card-text">Stock: {{ product.stock }}</p>
                <p class="card-text">Price: ${{ product.price }}</p>
              </div>

              <div v-else>
                <div class="mb-3">
                  <label for="editName">Product Name:</label>
                  <input v-model="product.editName" class="form-control" required>
                </div>

                <div class="mb-3">
                  <label for="editDescription">Description:</label>
                  <textarea v-model="product.editDescription" class="form-control" required></textarea>
                </div>

                <div class="mb-3">
                  <label for="editCategory">Category:</label>
                  <select v-model="product.editCategory.id" class="form-select" required>
                    <option value="" disabled>Select a category</option>
                    <option v-for="category in categories" :key="category.id" :value="category.id">
                      {{ category.name }}
                    </option>
                  </select>
                </div>

                <div class="mb-3">
                  <label for="editStock">Stock:</label>
                  <input type="number" v-model="product.editStock" class="form-control" required>
                </div>

                <div class="mb-3">
                  <label for="editPrice">Price:</label>
                  <input type="number" v-model="product.editPrice" class="form-control" required>
                </div>

                <div class="mb-3">
                  <label for="editImage">Image:</label>
                  <input type="file" @change="handleImageUpload(product, $event)" accept="image/*" class="form-control" required>
                </div>
              </div>

              <div class="text-center">
                <button class="btn btn-warning" @click="toggleEdit(product)" v-if="!product.edit">Edit</button>
                <button class="btn btn-success" @click="editProduct(product)" v-if="product.edit">Save</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
  /* Add your styling here */
  .card {
    max-width: 300px;
    margin: 0 auto;
  }

  .card-img-top {
    height: 100px;
    object-fit: cover;
  }
  .btn-warning {
    background-color: #ffc107;
    border-color: #ffc107;
  }

  .btn-warning:hover {
    background-color: #e0a800;
    border-color: #e0a800;
  }

  .btn-success {
    background-color: #28a745;
    border-color: #28a745;
  }

  .btn-success:hover {
    background-color: #218838;
    border-color: #218838;
  }
</style>

  
<script>
import NavBar from './NavBar.vue';
export default {
  name: 'EditProduct',
  components:{NavBar,},
  data() {
    return {
      products: [],
      categories: [],
      selectImage: null,
    };
  },
  mounted() {
    // Fetch product details
    this.fetchProductDetails();
    this.fetchCategories();
  },
  methods: {
    getImagePath(product) {
      return `http://localhost:5000/${product.image}`;
    },
    handleImageUpload(product, event) {
      if (event && event.target && event.target.files) {
        product.selectImage = event.target.files[0];
      }
    },


    async fetchProductDetails() {
      try {
        const response = await fetch(`http://localhost:5000/get-products`, {
          method: "GET",
          headers: {},
        });

        if (response.ok) {
          const data = await response.json();

          if (Array.isArray(data)) {
            // If the data is an array, use it directly
            this.products = data.map((product) => ({
              ...product,
              edit: false,
              editName: product.name,
              editDescription: product.description,
              editCategory: product.category,
              editPrice: product.price,
              editStock: product.stock,
              selectImage: null,
            }));
          } else {
            // If the data is an object, extract the array property
            const dataArray = data.products || [];
            this.products = dataArray.map((product) => ({
              ...product,
              edit: false,
              editName: product.name,
              editDescription: product.description,
              editCategory: {
                id: product.category.id,  // Make sure you are setting the correct property name
                name: product.category.name,
              },
              editPrice: product.price,
              editStock: product.stock,
              selectImage: null,
            }));
          }
        } else {
          console.log("cannot fetch product ", response.status);
        }
      } catch (error) {
        console.error("Error fetching product details:", error);
      }
    }
    ,

    fetchCategories() {
      fetch('http://localhost:5000/get-categories')
        .then(response => response.json())
        .then(data => {
          this.categories = data.categories;

        })
        .catch(error => console.error('Error fetching categories:', error));
    },

    toggleEdit(product) {
      product.edit = !product.edit
    },
    async editProduct(product) {
      try {
        const productId = product.id;
        const formData = new FormData();
        formData.append("name", product.editName);
        formData.append("description", product.editDescription);
        formData.append("category_id", product.editCategory.id);
        formData.append("price", product.editPrice);
        formData.append("stock", product.editStock);
        if (product.selectImage) {
          formData.append(
            "image",
            product.selectImage,
            product.selectImage.name
          );
        }
        const response = await fetch(
          `http://localhost:5000/edit-product/${productId}`,
          {
            method: "PUT",

            body: formData,
          }
        );
        if (response.ok) {
          product.name = product.editName;
          product.description = product.editDescription;
          product.category.id = product.editCategory.id;
          product.price = product.editPrice;
          product.stock = product.editStock;
          product.selectImage = null;
          product.edit = false;
          window.location.reload();
        } else {
          console.error("Failed to update product:", response.status);
        }
      } catch (error) {
        console.error("An error occurred:", error);
      }



    },

  },
};
</script>
  