<template>
    <form @submit.prevent="findRandomRestaurant" class="container mt-4">
        <div class="d-grid gap-3">
            <!-- Section du rayon -->
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

            <!-- Section des coordonnées -->
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

            <!-- Affichage des erreurs -->
            <div v-if="error" class="alert alert-danger">
                {{ error }}
            </div>

            <!-- Bouton de soumission -->
            <button type="submit" class="btn btn-primary" :disabled="isLoading">
                <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                {{ isLoading ? 'Searching...' : 'Find Random Restaurant' }}
            </button>
        </div>
    </form>
</template>

<script setup>
import { ref, defineEmits } from 'vue';

const X_API_KEY = import.meta.env.VITE_X_API_KEY;
const radius = ref(1000);
const latitude = ref(null);
const longitude = ref(null);
const isLoading = ref(false);
const error = ref(null);

const emit = defineEmits(["updateResults"]);

const findRandomRestaurant = async () => {
    try {
        isLoading.value = true;
        error.value = null; // Réinitialise l'erreur avant chaque requête

        const response = await fetch(
            `https://random-restaurant-flask-api-273942888807.asia-northeast1.run.app/random-restaurant?radius=${radius.value}&latitude=${latitude.value}&longitude=${longitude.value}&maxPhotos=20&X-API-KEY=${X_API_KEY}`,
            {
                method: "GET",

            }
        );

        // Vérifie si la réponse est OK
        if (!response.ok) {
            const errorData = await response.json(); // Essaie de récupérer le message d'erreur de l'API
            throw new Error(errorData.error || "Erreur lors de la récupération des données");
        }

        const data = await response.json();
        emit("updateResults", data); // Émet les résultats vers le parent
    } catch (err) {
        console.error("Erreur API :", err);
        error.value = err.message; // Affiche le message d'erreur à l'utilisateur
    } finally {
        isLoading.value = false;
    }
};

const getUserLocation = () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                // Récupère la latitude et la longitude de l'utilisateur
                latitude.value = position.coords.latitude;
                longitude.value = position.coords.longitude;
            },
            (err) => {
                // Gère les erreurs, par exemple si l'utilisateur refuse la demande
                console.error("Geolocation error: ", err);
                error.value = "Impossible de récupérer votre localisation. Veuillez entrer les coordonnées manuellement.";
            }
        );
    } else {
        error.value = "La géolocalisation n'est pas supportée par votre navigateur.";
    }
};
</script>

<style scoped>
/* Tu peux ajouter des styles personnalisés ici si nécessaire */
</style>