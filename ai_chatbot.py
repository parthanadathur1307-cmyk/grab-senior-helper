import google.auth
from google.gemini import GeminiClient

class RestaurantAssistant:
    def __init__(self):
        credentials, _ = google.auth.default()
        self.client = GeminiClient(credentials=credentials)

    def search_restaurant(self, query, location):
        # Use the Gemini AI to find restaurants based on the query and location
        response = self.client.search(query=query, location=location)
        return response

    def get_menu_recommendations(self, restaurant_id):
        # Get menu recommendations for a specific restaurant
        response = self.client.get_recommendations(restaurant_id=restaurant_id)
        return response

# Example usage:
# assistant = RestaurantAssistant()
# results = assistant.search_restaurant('Italian restaurant', 'New York')
# recommendations = assistant.get_menu_recommendations(results[0]['id'])