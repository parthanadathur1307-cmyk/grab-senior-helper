import requests

class GoogleGeminiAI:
    def __init__(self, api_key):
        self.api_key = api_key

    def search_restaurant(self, query):
        url = f"https://api.googleapis.com/gemini/restaurant?query={query}&key={self.api_key}"
        response = requests.get(url)
        return response.json()

    def search_menu(self, restaurant_id):
        url = f"https://api.googleapis.com/gemini/menu?restaurant_id={restaurant_id}&key={self.api_key}"
        response = requests.get(url)
        return response.json()


def main():
    api_key = 'YOUR_API_KEY_HERE'
    gemini_ai = GoogleGeminiAI(api_key)

    restaurant_query = input("Enter the name of the restaurant: ")
    results = gemini_ai.search_restaurant(restaurant_query)
    print("Restaurant Search Results:", results)

    restaurant_id = input("Enter the restaurant ID for menu search: ")
    menu_results = gemini_ai.search_menu(restaurant_id)
    print("Menu Search Results:", menu_results)

if __name__ == '__main__':
    main()