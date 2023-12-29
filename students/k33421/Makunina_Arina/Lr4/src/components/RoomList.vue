<template>
    <div>
      <h2>Room List</h2>
      <ul>
        <li v-for="room in rooms" :key="room.id">{{ room.name }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        rooms: [],
      };
    },
    mounted() {
      axios.get('/api/rooms/')
        .then(response => {
          this.rooms = response.data;
        })
        .catch(error => {
          console.error('Error fetching room data:', error);
        });
    },
  };
  </script>
  