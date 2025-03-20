<template>
    <form @submit.prevent="findRandomRestaurant" class="container mt-4">
        <div class="d-grid gap-3">

            <div class="row">
                <!-- Condition section (Open Now et Vegetarian) -->
                <div class="col-12 col-md-2">
                    <div class="form-check form-switch">
                        <input class="form-check-input" type="checkbox" role="switch" v-model="isOpen" checked>
                        <label class="form-check-label" for="flexSwitchCheckChecked">Open Now</label>
                    </div>

                    <div class="form-check form-switch">
                        <input class="form-check-input" type="checkbox" role="switch" v-model="isVegetarian">
                        <label class="form-check-label" for="flexSwitchCheckChecked">Vegetarian</label>
                    </div>
                </div>

                <!-- Radius section à droite -->
                <div class="col-12 col-md-10">
                    <div class="mb-3">
                        <label class="form-label">Radius: {{ radius }}m</label>
                        <input
                            class="form-range"
                            type="range"
                            v-model="radius"
                            min="100"
                            max="3000"
                        />
                    </div>
                </div>
            </div>

            <!-- Coordinate section -->
            <div class="input-group mb-3">
                <input
                    type="number"
                    step="any"
                    class="form-control"
                    placeholder="Latitude"
                    v-model="latitude"
                    required
                />
                <input
                    type="number"
                    step="any"
                    class="form-control"
                    placeholder="Longitude"
                    v-model="longitude"
                    required
                />
                <button
                    @click.prevent="getUserLocation"
                    class="btn btn-outline-secondary"
                    type="button"
                >
                    Get My Location
                </button>
            </div>

            

            <!-- Submit button -->
            <button type="submit" class="btn btn-primary" :disabled="isLoading">
                <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                {{ isLoading ? 'Searching...' : 'Find Random Restaurant' }}
            </button>

            <!-- Error display -->
            <div v-if="error" class="alert alert-danger">
                {{ error }}
            </div>
        </div>
    </form>
</template>

<script setup>
import { ref, defineEmits } from 'vue';
import { useHistoryStore } from "@/stores/useHistoryStore";

const historyStore = useHistoryStore();

const X_API_KEY = import.meta.env.VITE_X_API_KEY;
const API_URL = import.meta.env.VITE_API_URL;
const radius = ref(1000);
const latitude = ref(null);
const longitude = ref(null);
const isLoading = ref(false);
const error = ref(null);
const isOpen = ref(true);
const isVegetarian = ref(false);

const emit = defineEmits(["updateResults"]);

const findRandomRestaurant = async () => {
    try {
        isLoading.value = true;
        error.value = null;

        const response = await fetch(API_URL + "/random-restaurant", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-API-KEY': X_API_KEY,
            },
            body: JSON.stringify({
                'radius': radius.value,
                'latitude': latitude.value,
                'longitude': longitude.value,
                'maxPhotos': 10,
                'isOpen': isOpen.value,
                'isVegetarian': isVegetarian.value,
                'restaurantsHistory': historyStore.restaurants.map(restaurant => restaurant.placeInfos.address),
            }),
        });

        if (!response.ok) {
            const errorData = await response.json(); // Essaie de récupérer le message d'erreur de l'API
            throw new Error(errorData.error || "Erreur lors de la récupération des données");
        }

        const data = await response.json();
        historyStore.addRestaurant(data);

        emit("updateResults", data);
    } catch (err) {
        console.error("Erreur API :", err);
        error.value = err.message;
    } finally {
        isLoading.value = false;
    }
};

const getUserLocation = () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                latitude.value = position.coords.latitude;
                longitude.value = position.coords.longitude;
            },
            (err) => {
                console.error("Geolocation error: ", err);
                error.value = "Unable to retrieve your location. Please enter coordinates manually";
            }
        );
    } else {
        error.value = "Geolocation is not supported by your browser";
    }
};
</script>

<style scoped>
</style>