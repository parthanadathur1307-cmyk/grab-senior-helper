import requests

class Chatbot:
    def __init__(self):
        self.api_key = 'YOUR_GOOGLE_GENERATIVE_AI_API_KEY'
        self.base_url = 'https://api.google.com/generative-ai'

    def process_request(self, user_input):
        response = requests.post(self.base_url, headers={'Authorization': f'Bearer {self.api_key}'}, json={
            'query': user_input
        })
        return response.json()

    def recommend_dishes(self, user_preferences):
        request_input = f'Recommend me dishes based on the following preferences: {user_preferences}'
        response = self.process_request(request_input)
        return response.get('dishes', [])

# Example usage:
if __name__ == '__main__':
    chatbot = Chatbot()
    preferences = "vegetarian and spicy"
    recommendations = chatbot.recommend_dishes(preferences)
    print(f'Recommended dishes: {recommendations}')