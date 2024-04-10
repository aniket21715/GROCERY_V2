<template>
  <div>
    <NavBar/>
    <div class="container mt-4">
      <h2 class="text-center mb-4">Admin Dashboard</h2>

      <!-- Pending Requests Section -->
      <div v-if="pendingRequests.length > 0" class="card mb-4">
        <div class="card-header">
          <h3 class="card-title">Pending Requests</h3>
        </div>
        <div class="card-body">
          <div v-for="request in pendingRequests" :key="request.id" class="mb-3">
            <span>{{ request.username }} -- {{ request.status }} </span>
            <button @click="approveRequest(request.id)" class="btn btn-success">Approve...</button>
            <button @click="rejectRequest(request.id)" class="btn btn-danger">Reject...</button>
          </div>
        </div>
      </div>

      <!-- All Requests Section -->
      <div v-if="allRequests.length > 0" class="card mb-4">
        <div class="card-header">
          <h3 class="card-title">All Requests</h3>
        </div>
        <div class="card-body">
          <div v-for="request in allRequests" :key="request.id" class="mb-3">
            <span>{{ request.username }} - {{ request.status }}</span>
            <button @click="approveRequest(request.id)" class="btn btn-success">Approve...</button>
            <button @click="rejectRequest(request.id)" class="btn btn-danger">Reject...</button>
          </div>
        </div>
      </div>
      <div v-if="categoryRequests.length > 0" class="card mb-4">
      <div class="card-header">
        <h3 class="card-title">Category Requests</h3>
      </div>
      <div class="card-body">
        <div v-for="request in categoryRequests" :key="request.id" class="mb-3">
          <span>{{ request.store_manager_username }} - {{ request.category_name }} - {{ request.status }} </span>
          <button @click="approveCategoryRequest(request.id)" class="btn btn-success">Approve...</button>
          <button @click="rejectCategoryRequest(request.id)" class="btn btn-danger">Reject...</button>
        </div>
      </div>
      </div>

      <!-- Categories Section -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Categories</h3>
        </div>
        <div class="card-body">
          <button @click="goToAddCategory" class="btn btn-primary mb-3">Add Category</button>

          <ul class="list-group">
            <li v-for="category in categories" :key="category.id" class="list-group-item d-flex justify-content-between align-items-center">
              {{ category.name }} - {{ category.description }}
              <div>
                <button @click="editCategory(category)" class="btn btn-info btn-sm">Edit</button>
                <button @click="deleteCategory(category.id)" class="btn btn-danger btn-sm">Delete</button>
              </div>
            </li>
          </ul>
        </div>
      </div>
      <div>
    <h2>Received Messages</h2>
      <div v-if="messages.length > 0">
        <div v-for="message in messages" :key="message.id" class="message-container">
          <div>
            <strong>From:</strong> {{ message.sender.username }}
          </div>
          <div>
            <strong>Content:</strong> {{ message.content }}
          </div>
          <div>
            <strong>Timestamp:</strong> {{ message.timestamp }}
          </div>
          <button v-if="!message.read" @click="markAsRead(message.id)" class="btn btn-primary btn-sm">Mark as Read</button>
        </div>
      </div>
      <div v-else>
        <p>No messages available.</p>
      </div>
    </div>
    </div>
  </div>
</template>

<script>

  import NavBar from '@/components/NavBar.vue';

  export default {
    name: 'AdminDashboard',
    components: {
    NavBar,
   },
  data() {
    return {
      pendingRequests: [],
      allRequests: [],
      categories: [],
      categoryRequests: [],
      messages: [],
    };
  },
  mounted() {
    // Fetch pending store manager registration requests on component mount
    fetch('http://localhost:5000/admin/dashboard')
      .then(response => response.json())
      .then(data => {
        this.pendingRequests = data.pendingRequests;
      })
      .catch(error => console.error('Error:', error));

    // Fetch all store manager registration requests on component mount
    fetch('http://localhost:5000/admin/all-requests')
      .then(response => response.json())
      .then(data => {
        this.allRequests = data.allRequests;
      })
      .catch(error => console.error('Error:', error));
    this.fetchCategories();
    this.fetchCategoryRequests();
    this.fetchMessages();

  },
  methods: {
  
    fetchPendingRequests() {
      // Fetch pending store manager registration requests
      fetch('http://localhost:5000/admin/dashboard')
        .then(response => response.json())
        .then(data => {
          this.pendingRequests = data.pendingRequests;
        })
        .catch(error => console.error('Error:', error));
    },
    approveRequest(requestId) {
      // Send request to approve the store manager registration
      fetch(`http://localhost:5000/admin/approve-store-manager/${requestId}`, {
        method: 'PUT',
      })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          // Refresh the requests after approval
          this.fetchAllRequests();
        })
        .catch(error => console.error('Error:', error));
    },
    rejectRequest(requestId) {
      // Send request to reject the store manager registration
      fetch(`http://localhost:5000/admin/reject-store-manager/${requestId}`, {
        method: 'PUT',
      })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          // Refresh the requests after rejection
          this.fetchAllRequests();
        })
        .catch(error => console.error('Error:', error));
    },
    fetchAllRequests() {
      // Fetch all store manager registration requests
      fetch('http://localhost:5000/admin/all-requests')
        .then(response => response.json())
        .then(data => {
          this.allRequests = data.allRequests;
        })
        .catch(error => console.error('Error:', error));
    },
    goToAddCategory() {
      // Redirect to AddCategory.vue
      this.$router.push('/AddCategory');
    },

    fetchCategories() {
      // Fetch categories from the backend
      fetch('http://localhost:5000/get-categories')
        .then(response => response.json())
        .then(data => {
          console.log(data);
          this.categories = data.categories;
          console.log('this is hhhhh',this.categories)
        })
        .catch(error => console.error('Error:', error));
    },
    editCategory(category) {
      const newName = prompt('Enter the new name:', category.name);
      const newDescription = prompt('Enter the new description:', category.description);

      if (newName !== null && newDescription !== null) {
        // Make a PUT request to update the category
        fetch(`http://localhost:5000/edit-category/${category.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: newName,
            description: newDescription,
          }),
        })
          .then(response => response.json())
          .then(data => {
            console.log(data);
            // Refresh the categories after editing
            this.fetchCategories();
          })
          .catch(error => console.error('Error:', error));
      }
    },
    deleteCategory(categoryId) {
      const confirmDelete = confirm('Are you sure you want to delete this category?');
      
      if (confirmDelete) {
        // Make a DELETE request to remove the category
        fetch(`http://localhost:5000/delete-category/${categoryId}`, {
          method: 'DELETE',
        })
          .then(response => response.json())
          .then(data => {
            console.log(data);
            // Refresh the categories after deletion
            this.fetchCategories();
          })
          .catch(error => console.error('Error:', error));
      }
    },
    fetchCategoryRequests() {
    // Fetch category requests from the backend
    fetch('http://localhost:5000/admin/category-requests')
      .then(response => response.json())
      .then(data => {
        console.log("Category Requests:", data.categoryRequests);
        this.categoryRequests = data.categoryRequests;
      })
      .catch(error => console.error('Error:', error));
  },
  approveCategoryRequest(requestId) {
    fetch(`http://localhost:5000/admin/approve-category-request/${requestId}`, {
      method: 'PUT',
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        // Remove the approved category request from the array
        this.categoryRequests = this.categoryRequests.filter(request => request.id !== requestId);
      })
      .catch(error => console.error('Error:', error));
  },

  rejectCategoryRequest(requestId) {
    fetch(`http://localhost:5000/admin/reject-category-request/${requestId}`, {
      method: 'PUT',
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        // Remove the rejected category request from the array
        this.categoryRequests = this.categoryRequests.filter(request => request.id !== requestId);
      })
      .catch(error => console.error('Error:', error));
  },
  async fetchMessages() {
      try {
        const response = await fetch('http://localhost:5000/get-messages', {
          method: 'GET',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'), // Assuming you handle authentication with JWT
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.messages = data.messages;
        } else {
          console.error('Failed to fetch messages', response.status);
        }
      } catch (error) {
        console.error('Error fetching messages', error);
      }
    },
    
    markAsRead(messageId) {
  // Make a request to mark the message as read
  fetch(`http://localhost:5000/mark-as-read/${messageId}`, {
    method: 'PUT',
    headers: {
      'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
    },
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      // Remove the message from the messages array
      this.messages = this.messages.filter(message => message.id !== messageId);
    })
    .catch(error => console.error('Error marking as read:', error));
},

  },
};
</script>

<style scoped>
  /* Add your styling here */

  .btn-success {
    background-color: #28a745;
    border-color: #28a745;
  }

  .btn-success:hover {
    background-color: #218838;
    border-color: #218838;
  }

  .btn-danger {
    background-color: #dc3545;
    border-color: #dc3545;
  }

  .btn-danger:hover {
    background-color: #bd2130;
    border-color: #bd2130;
  }

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

  .message-container {
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 10px;
  }
</style>





