import streamlit as st
from database_module import Database
from menu_parser import MenuParser
from chatbot_module import Chatbot

# Initialize the database
db = Database()  

# Load menu data
menu_data = MenuParser().parse_menu()  

# Initialize the chatbot
chatbot = Chatbot()  

# Streamlit user interface
st.title('Senior Citizen Helper')

# Display menu options
st.header('Available Menu Options')
for item in menu_data:
    st.write(item)

# Chatbot interaction
st.header('Chat with our AI Assistant')
user_input = st.text_input('You:', '')  
if st.button('Send'):
    response = chatbot.get_response(user_input)
    st.write('AI Assistant:', response)