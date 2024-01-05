<template>
  <div class="container mt-4">
    <div class="card">
      <div class="card-header">
        <h2>Add Category</h2>
      </div>
      <div class="card-body">
        <form @submit.prevent="addCategory">
          <div class="mb-3">
            <label for="name" class="form-label">Category Name:</label>
            <input type="text" class="form-control" v-model="name" required>
          </div>
          <div class="mb-3">
            <label for="description" class="form-label">Description:</label>
            <textarea class="form-control" v-model="description" required></textarea>
          </div>
          <button type="submit" class="btn btn-primary">Add Category</button>
        </form>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'AddCategory',
  data() {
    return {
      name: '',
      description: '',
    };
  },
  methods: {
    addCategory() {
      fetch('http://localhost:5000/add-category', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: this.name,
          description: this.description,
        }),
      })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          // Handle successful category addition
          // You can redirect or show a success message
          this.$router.push('/AdminDashboard');
        })
        .catch(error => console.error('Error:', error));
    },
  },
};
</script>
