import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

import { createApp } from 'vue'
import App from './App.vue'
import SearchParams from './components/SearchParams.vue'
import RestaurantDisplay from './components/RestaurantDisplay.vue'


const app = createApp(App)
app.component('search-params', SearchParams)
app.component('restaurant-display', RestaurantDisplay)
app.mount('#app')
