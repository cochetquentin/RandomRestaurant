from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_caching import Cache
import requests
import random
import base64
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
X_API_KEY = os.getenv('X_API_KEY')

app = Flask(__name__)
CORS(app)
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)
cache.init_app(app)

@app.before_request
def check_api_key():
    if request.method == "OPTIONS":
        return  # Let flask handle OPTIONS requests

    key = request.headers.get("X-API-KEY")
    if key != X_API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    
@app.route('/')
def index():
    return 'API Online !'

def fetch_photo_urls(restaurant, max_photos=5):
    """ Génère les URLs des photos en réduisant leur taille. """
    return [
        f"https://places.googleapis.com/v1/{photo['name']}/media?key={GOOGLE_PLACES_API_KEY}&maxHeightPx=1080&maxWidthPx=1920"
        for photo in restaurant.get('photos', [])[:max_photos]
    ]

def fetch_photos_base64(photo_urls):
    """ Télécharge les images en parallèle et les encode en Base64. """
    def download_image(url):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return base64.b64encode(response.content).decode('utf-8')
        except requests.RequestException:
            return None
    
    with ThreadPoolExecutor() as executor:
        photos = list(executor.map(download_image, photo_urls))
    return [f"data:image/jpeg;base64,{photo}" for photo in photos if photo]

@cache.memoize(timeout=3600)
def get_photos(photo_urls, use_base64=True):
    """ Gère la récupération des photos avec mise en cache. """
    return fetch_photos_base64(photo_urls) if use_base64 else photo_urls

def filter_restaurants(restaurants, isOpen, isVegetarian, restaurantsHistory):
    """ Filtre les restaurants en fonction des critères. """
    return [
        restaurant for restaurant in restaurants
        if (not isOpen or restaurant.get('currentOpeningHours', {}).get('openNow', False))
        and (not isVegetarian or restaurant.get('servesVegetarianFood', False))
        and restaurant.get('formattedAddress', 'Unknown') not in restaurantsHistory
    ]

@app.route('/random-restaurant', methods=['POST'])
def random_restaurant():
    print("Request received")
    try:
        data = request.get_json()
        lat = float(data.get('latitude', None))
        lng = float(data.get('longitude', None))
        radius = float(data.get('radius', None))
        isOpen = data.get('isOpen', False)
        isVegetarian = data.get('isVegetarian', False)
        maxPhotos = data.get('maxPhotos', 5)
        use_base64 = data.get('useBase64', True)
        restauransHistory = data.get('restaurantsHistory', [])

        if not lat or not lng or not radius:
            return jsonify({"error": "Missing or invalid parameters"}), 400
        if radius < 100 or radius > 3000:
            return jsonify({"error": "Radius must be between 100 and 3000 meters"}), 400

        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': GOOGLE_PLACES_API_KEY,
            'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.currentOpeningHours,places.googleMapsUri,places.nationalPhoneNumber,places.rating,places.userRatingCount,places.reviews,places.photos'
        }
        json_data = {
            'includedTypes': ['restaurant'],
            'maxResultCount': 10,
            'locationRestriction': {
                'circle': {
                    'center': {'latitude': lat, 'longitude': lng},
                    'radius': radius,
                },
            },
        }
        response = requests.post('https://places.googleapis.com/v1/places:searchNearby', headers=headers, json=json_data)
        
        if not response.ok:
            return jsonify({"error": "Google Places API error"}), response.status_code

        restaurants = response.json().get('places', [])
        if not restaurants:
            return jsonify({"error": "No restaurants found"}), 404

        restaurants = filter_restaurants(restaurants, isOpen, isVegetarian, restauransHistory)
        if not restaurants:
            return jsonify({"error": "No restaurants found matching the criteria"}), 404
        
        restaurant = random.choice(restaurants)
        place_info = {
            'name': restaurant.get('displayName', {}).get('text', 'Unknown'),
            'address': restaurant.get('formattedAddress', 'Unknown'),
            'primaryType': restaurant.get('primaryTypeDisplayName', {}).get('text', 'Unknown'),
            'isOpen': restaurant.get('currentOpeningHours', {}).get('openNow', False),
            'isVegetarian': restaurant.get('servesVegetarianFood', False),
            'isGoodForWatchingSports': restaurant.get('goodForWatchingSports', False),
            'isGoodForGroups': restaurant.get('goodForGroups', False),
            'openSchedule': restaurant.get('currentOpeningHours', {}).get('weekdayDescriptions', []),
            'mapLink': restaurant.get('googleMapsUri', ''),
            'phoneNumber': restaurant.get('nationalPhoneNumber', ''),
            'rating': restaurant.get('rating', 0),
            'ratingNumber': restaurant.get('userRatingCount', 0),
        }
        
        reviews = sorted(
            [
                {
                    'author': review.get('authorAttribution', {}).get('displayName', 'Anonymous'),
                    'comment': review.get('originalText', {}).get('text', ''),
                    'rating': review.get('rating', 0),
                    'timeAgo': review.get('relativePublishTimeDescription', '')
                }
                for review in restaurant.get('reviews', [])
            ],
            key=lambda x: x.get('timeAgo', ''),
            reverse=True
        )
        
        photo_urls = fetch_photo_urls(restaurant, max_photos=maxPhotos)
        photos = get_photos(photo_urls, use_base64)

        return jsonify({'placeInfos': place_info, 'reviews': reviews, 'photos': photos}), 200

    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        print(e)
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)