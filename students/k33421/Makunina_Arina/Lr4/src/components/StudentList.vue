<template>
    <div>
      <h2>Список студентов</h2>
      <ul>
        <li v-for="student in students" :key="student.id">
          {{ student.name }} - {{ student.group.name }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        students: [],
      };
    },
    mounted() {
      // Выполняем запрос к API при монтировании компонента
      axios.get('http://your-django-api-url/students/')
        .then(response => {
          this.students = response.data;
        })
        .catch(error => {
          console.error('Error fetching students:', error);
        });
    },
  };
  </script>
  
  <style scoped>
  </style>
  