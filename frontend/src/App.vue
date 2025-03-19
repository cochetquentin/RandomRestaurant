<template>
  <div class="container mt-4">
    <h1 class="text-center mb-4 display-1">Random Restaurant Finder</h1>
    <search-params @updateResults="handleResults" />
    <restaurant-display :restaurant="restaurant"  />
    <restaurant-history @updateResults="handleResults" />
  </div> 
</template>

<script setup>
import { ref } from 'vue';
const restaurant = ref(null);  

const handleResults = (data) => {
  restaurant.value = data;
};
</script>


<style>
</style>
