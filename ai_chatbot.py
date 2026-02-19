import requests

class Chatbot:
    def __init__(self, dietary_restrictions, price_range, user_language):
        self.dietary_restrictions = dietary_restrictions
        self.price_range = price_range
        self.user_language = user_language
        self.supported_languages = ['English', 'Chinese', 'Malay', 'Tamil']

    def search_restaurants(self, user_request):
        # Placeholder for API integration (e.g., Yelp API)
        response = self._api_call(user_request)
        return self._parse_response(response)

    def _api_call(self, user_request):
        # Mock API call function, replace with actual API integration
        # Example: return requests.get('API_URL').json()
        return {
            'restaurants': [{'name': 'Restaurant 1', 'menu': ['Dish 1', 'Dish 2']}, {'name': 'Restaurant 2', 'menu': ['Dish 3', 'Dish 4']}],
            'success': True
        }

    def _parse_response(self, response):
        if response['success']:
            return response['restaurants']
        return []

    def get_recommendations(self, user_request):
        restaurants = self.search_restaurants(user_request)
        recommendations = []
        for restaurant in restaurants:
            recommendations.append({
                'name': restaurant['name'],
                'menu': restaurant['menu']
            }) 
        return recommendations

# Example usage
if __name__ == '__main__':
    user = Chatbot(dietary_restrictions='Vegetarian', price_range='10-20', user_language='English')
    user_request = "Find restaurants that serve vegetarian food within my price range."
    recommendations = user.get_recommendations(user_request)
    print(recommendations)