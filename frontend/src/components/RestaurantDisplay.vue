<template>
    <div v-if="restaurant && restaurant.placeInfos" class="container mt-4">
        <h2 class="text-center mb-4 display-3">{{ restaurant.placeInfos.name }}</h2>
        
        <div class="card mb-4">
            <div class="card-body">
                <p class="card-text"><strong>Address:</strong> {{ restaurant.placeInfos.address }}</p>
                <p class="card-text"><strong>Open Now:</strong> {{ restaurant.placeInfos.isOpen ? 'Yes' : 'No' }}</p>
                <p class="card-text"><strong>Type:</strong> {{ restaurant.placeInfos.primaryType }}</p>
                <p class="card-text"><strong>Rating:</strong> {{ restaurant.placeInfos.rating }} ⭐ ({{ restaurant.placeInfos.ratingNumber }} reviews)</p>
                <p class="card-text"><strong>Good for Groups:</strong> {{ restaurant.placeInfos.isGoodForGroups ? 'Yes' : 'No' }}</p>
                <p class="card-text"><strong>Good for Watching Sports:</strong> {{ restaurant.placeInfos.isGoodForWatchingSport ? 'Yes' : 'No' }}</p>
                <p class="card-text"><strong>Vegetarian Options:</strong> {{ restaurant.placeInfos.isServingVegetarianFood ? 'Yes' : 'No' }}</p>
                <p class="card-text"><strong>Phone Number:</strong> {{ restaurant.placeInfos.phoneNumber || 'Not available' }}</p>
                <p class="card-text">
                    <a :href="restaurant.placeInfos.mapLink" target="_blank" class="btn btn-primary">
                        View on Google Maps
                    </a>
                </p>
            </div>
        </div>

        <div class="card mb-4">
            <div class="card-body">
                <h3 class="card-title display-5">Opening Hours:</h3>
                <ul class="list-group list-group-flush">
                    <li v-for="(day, index) in restaurant.placeInfos.openSchedule" :key="index" class="list-group-item">{{ day }}</li>
                </ul>
            </div>
        </div>

        <!-- Photos section -->
        <div v-if="restaurant.photos && restaurant.photos.length" class="card mb-4">
            <div class="card-body">
                <h3 class="card-title display-5">Photos:</h3>
                <div id="photoCarousel" class="carousel slide" data-bs-ride="carousel" ref="carousel">
                    <div class="carousel-inner">
                        <div v-for="(photo, index) in restaurant.photos" :key="index" :class="['carousel-item', { 'active': index === 0 }]">
                            <img :src="photo" class="d-block w-100" alt="Restaurant photo">
                        </div>
                    </div>
                    <button class="carousel-control-prev" type="button" data-bs-target="#photoCarousel" data-bs-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span class="visually-hidden">Previous</span>
                    </button>
                    <button class="carousel-control-next" type="button" data-bs-target="#photoCarousel" data-bs-slide="next">
                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                        <span class="visually-hidden">Next</span>
                    </button>
                </div>
            </div>
        </div>

        <div class="card mb-4">
            <div class="card-body">
                <h3 class="card-title display-5">Reviews:</h3>
                <ul v-if="restaurant.reviews && restaurant.reviews.length" class="list-group list-group-flush">
                    <li v-for="(review, index) in restaurant.reviews" :key="index" class="list-group-item">
                        <p><strong>{{ review.author }}</strong> ({{ review.rating }} ⭐) - {{ review.timeAgo }}</p>
                        <p>{{ review.comment }}</p>
                    </li>
                </ul>
                <p v-else class="card-text">No reviews available.</p>
            </div>
        </div>
    </div>
    <p v-if="restaurant && restaurant.error" class="text-center mt-4 alert alert-info">No restaurant found. Try adjusting your search parameters.</p>
</template>

<script setup>
import { onMounted, ref, nextTick, watch } from 'vue';

const props = defineProps({
    restaurant: Object
});

const carousel = ref(null);

onMounted(() => {
    nextTick(() => {
        if (carousel.value) {
            new bootstrap.Carousel(carousel.value);
        }
    });
});

// Create carousel when photos change
watch(
    () => props.restaurant?.photos,
    (newPhotos) => {
        if (newPhotos && newPhotos.length) {
            nextTick(() => {
                if (carousel.value) {
                    new bootstrap.Carousel(carousel.value);
                }
            });
        }
    },
    { deep: true }
);
</script>

<style scoped>
.carousel-item img {
    max-height: 400px;
    object-fit: cover;
}
</style>
