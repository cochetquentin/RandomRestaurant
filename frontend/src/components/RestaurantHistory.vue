<template>
  <div>
    <!-- Button to show/hide the panel -->
    <button @click="toggleHistory" class="btn btn-danger position-fixed top-0 end-0 m-3">
      📜 History
    </button>

    <!-- Overlay behind the panel to prevent clicks -->
    <div v-if="isOpen" class="overlay position-fixed top-0 start-0 w-100 h-100 bg-dark opacity-50" @click="toggleHistory"></div>

    <!-- Sliding panel -->
    <div class="history-panel bg-white border shadow-sm p-3 position-fixed top-0 end-0 vh-100 overflow-auto"
         :class="{ 'd-block': isOpen, 'd-none': !isOpen }">
      <h5 class="text-center">History</h5>
      <button @click="toggleHistory" class="btn-close position-absolute top-0 end-0 m-2"></button>
      <ul class="list-group mt-3">
        <li v-for="(restaurant, index) in historyStore.restaurants" :key="index"
            class="list-group-item" @click="getRestaurantFromHistory(restaurant)">
          {{ restaurant.placeInfos.name }}
        </li>
      </ul>
      <button @click="historyStore.clearHistory()" class="btn btn-warning w-100 mt-3">
        Clear History
      </button>
    </div>
  </div>
</template>


<script setup>
import { useHistoryStore } from "@/stores/useHistoryStore";
import { ref } from "vue";

const historyStore = useHistoryStore();
const isOpen = ref(false);

const emit = defineEmits(["updateResults"]);

function toggleHistory() {
  isOpen.value = !isOpen.value;
}

function getRestaurantFromHistory(restaurant) {
  emit("updateResults", restaurant);
  toggleHistory();
}
</script>



<style scoped>
.history-panel {
  width: 250px;
  transition: transform 0.3s ease-in-out;
  transform: translateX(100%);
  z-index: 1050; /* The panel is above the overlay */
}

.d-block {
  transform: translateX(0);
}

.overlay {
  z-index: 1040; /* The overlay is below the panel but above other elements */
  cursor: pointer; /* Shows a hand cursor to indicate it's clickable */
}

/* For the "click" effect on each list item */
.list-group-item:active {
  background-color: #f8d7da; /* Change background color when clicked */
  transform: scale(0.98); /* Slightly reduce the size of the element for the click effect */
  transition: transform 0.1s ease-in-out;
}
</style>
