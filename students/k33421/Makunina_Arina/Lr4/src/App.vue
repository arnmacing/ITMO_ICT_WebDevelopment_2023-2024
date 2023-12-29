<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
import { watch } from 'vue';
import { useAuthStore } from './store/index.js';

const authStore = useAuthStore();

watch(() => authStore.role, (currentRole) => {
  console.log(`Role changed to: ${currentRole}`);
});


const login = async () => {
  try {
    const formData = new FormData();
    formData.append('username', username.value);
    formData.append('password', password.value);

    const response = await fetch('/journal/api/token/', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      authStore.setToken(data.auth_token);
      authStore.setRole(data.role);

      // Redirect to the student's cabinet after successful login
      if (data.role === 'student') {
        router.push({ name: 'student-cabinet' });
      }

      console.log('Login successful');
    } else {
      console.error('Authentication failed');
    }
  } catch (error) {
    console.error('Error during authentication:', error);
  }
};

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1 {
  font-size: 2em;
  margin-bottom: 20px;
}
</style>
