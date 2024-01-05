<template>
  <NavBar/>
  <div>
    <h2>Admin Dashboard</h2>
    <div v-if="pendingRequests.length === 0">No pending requests</div>
    <div v-else>
      <div v-for="request in pendingRequests" :key="request.id">
        <span>{{ request.username }} - {{ request.status }}</span>
        <button @click="approveRequest(request.id)">Approve</button>
        <button @click="rejectRequest(request.id)">Reject</button>
      </div>
    </div>
  </div>
  <div v-if="allRequests.length === 0">No requests</div>
    <div v-else>
      <div v-for="request in allRequests" :key="request.id">
        <span>{{ request.username }} - {{ request.status }}</span>
        <button @click="approveRequest(request.id)">Approve</button>
        <button @click="rejectRequest(request.id)">Reject</button>
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
  },
};
</script>

  