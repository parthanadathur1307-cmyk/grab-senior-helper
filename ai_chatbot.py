import google.generativeai as genai

class AIChatbot:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def search_restaurants(self, user_request, restaurants_data, language='english'):
        """
        Use AI to search for restaurants based on user request
        Considers dietary restrictions and price preferences
        """
        prompt = f"""
        User request: {user_request}
        Language: {language}
        
        Available restaurants data:
        {restaurants_data}
        
        Based on the user's request, recommend the best restaurant and dish.
        Consider:
        - Food preference (e.g., chicken rice, fish dishes)
        - Dietary restrictions if mentioned
        - Price preferences if mentioned
        - Rating of restaurants
        
        Provide a clear recommendation with restaurant name, dish, price, and reason.
        Keep response simple for senior citizens.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def search_menu_items(self, user_request, menu_data, language='english'):
        """
        Use AI to search for specific items in uploaded menus
        """
        prompt = f"""
        User request: {user_request}
        Language: {language}
        
        Available menu items:
        {menu_data}
        
        Find and recommend dishes that match the user's request.
        Consider dietary restrictions and price preferences if mentioned.
        Provide dish name, description, and price.
        Keep response simple and clear.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def translate_request(self, text, target_language='english'):
        """
        Translate user input to English for processing
        Supports: English, Chinese, Malay, Tamil
        """
        prompt = f"""
        Translate the following text to English.
        Original language may be: English, Chinese, Malay, or Tamil.
        
        Text: {text}
        
        Provide only the English translation.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def chat(self, user_message, context=""):
        """
        General chat functionality for the senior citizen
        """
        prompt = f"""
        You are a helpful assistant for senior citizens in Singapore using GRAB delivery service.
        Be polite, clear, and use simple language.
        Avoid technical jargon.
        
        Context: {context}
        User message: {user_message}
        
        Provide a helpful response in simple words.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
