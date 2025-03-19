import { defineStore } from "pinia";

export const useHistoryStore = defineStore("history", {
    state: () => ({
        restaurants: [],
    }),
    actions: {
        addRestaurant(restaurant) {
            this.restaurants.push(restaurant);
        },
        clearHistory() {
            this.restaurants = [];
        },
    },
});
