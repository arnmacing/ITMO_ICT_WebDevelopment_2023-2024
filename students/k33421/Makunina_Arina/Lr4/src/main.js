// main.js
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import { createVuetify } from 'vuetify'; 
import 'vuetify/styles'; 

const pinia = createPinia();
const vuetify = createVuetify({
  // Any Vuetify options
});
const app = createApp(App);

app.use(pinia);
app.use(vuetify);
app.use(router);

app.mount('#app');
