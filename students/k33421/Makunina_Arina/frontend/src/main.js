import Vue from 'vue';
import App from './App.vue';
import vuetify from './plugins/vuetify';
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'


new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app');
