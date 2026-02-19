import streamlit as st
import google.generativeai as genai
from database import Database
from menu_parser import extract_menu_items
import os

# Page configuration for senior citizens - large fonts and simple interface
st.set_page_config(
    page_title="GRAB Senior Helper",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for larger text
st.markdown("""
    <style>
    html, body, [class*="st-"] {
        font-size: 20px;
    }
    h1 {
        font-size: 48px;
    }
    h2 {
        font-size: 36px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'restaurants' not in st.session_state:
    st.session_state.restaurants = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Initialize database
db = Database('grab_helper.db')

# Initialize AI chatbot with Google Gemini
api_key = os.getenv('GOOGLE_API_KEY', 'YOUR_API_KEY_HERE')
if api_key != 'YOUR_API_KEY_HERE':
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None
    st.warning("⚠️ Please set GOOGLE_API_KEY environment variable")

# Language support
LANGUAGES = {
    'English': 'english',
    '中文 (Chinese)': 'chinese',
    'Bahasa Melayu': 'malay',
    'தமிழ் (Tamil)': 'tamil'
}

# Main title
st.title("🍽️ GRAB Senior Helper")
st.subheader("Find Your Favorite Food - Easy to Use!")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    selected_language = st.selectbox("Choose Your Language", list(LANGUAGES.keys()))
    language_code = LANGUAGES[selected_language]
    
    st.divider()
    st.header("📋 Quick Links")
    page = st.radio("Select an option:", 
                     ["🏠 Home", "🤖 Food Chatbot", "📄 Upload Menu", "📊 My Orders"])

# HOME PAGE
if page == "🏠 Home":
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://via.placeholder.com/300x200?text=GRAB+Senior+Helper", use_column_width=True)
    
    with col2:
        st.markdown("""
        ### Welcome to GRAB Senior Helper! 👋
        
        This app helps you:
        - 🤖 Chat with our AI to find food you love
        - 📄 Upload restaurant menus
        - 💰 Set your budget
        - ❌ Avoid foods you can't eat
        - ⭐ Find the best rated restaurants
        
        **Start by selecting an option from the menu on the left!**
        """)
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Restaurants", len(st.session_state.restaurants), "+5 new this week")
    with col2:
        st.metric("Menu Items", 250, "+50 new items")
    with col3:
        st.metric("Happy Seniors", 1200, "+100 this month")

# FOOD CHATBOT PAGE
elif page == "🤖 Food Chatbot":
    st.header("🤖 AI Food Assistant")
    st.write("Tell me what you want to eat, and I'll find the best options for you!")
    
    # User input for food preference
    user_input = st.text_area("What would you like to eat? (e.g., 'I want chicken rice, not expensive')", 
                              placeholder="Type here in your preferred language...",
                              height=100)
    
    # Dietary restrictions
    col1, col2 = st.columns(2)
    with col1:
        dietary_restrictions = st.multiselect(
            "Any foods you can't eat?",
            ["Pork", "Beef", "Seafood", "Nuts", "Dairy", "Spicy", "None"]
        )
    
    with col2:
        price_range = st.select_slider(
            "Price range per item (SGD)",
            options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20],
            value=(3, 10)
        )
    
    if st.button("🔍 Search", use_container_width=True):
        if user_input and model:
            with st.spinner("Finding the best options for you..."):
                prompt = f"""
                User request: {user_input}
                Language: {language_code}
                Dietary restrictions to avoid: {', '.join(dietary_restrictions) if dietary_restrictions else 'None'}
                Price range: ${price_range[0]} - ${price_range[1]} SGD
                
                Recommend:
                1. Restaurant name
                2. Dish name and description
                3. Price
                4. Why this is a good choice for them
                
                Format the response in a friendly, encouraging way for a senior citizen.
                """
                
                response = model.generate_content(prompt)
                st.success("Here are my recommendations:")
                st.info(response.text)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "user": user_input,
                    "bot": response.text
                })
        elif not model:
            st.error("AI model not available. Please set GOOGLE_API_KEY.")
        else:
            st.warning("Please type what you want to eat first!")

# UPLOAD MENU PAGE
elif page == "📄 Upload Menu":
    st.header("📄 Upload Restaurant Menu")
    st.write("Upload a PDF menu, and our AI will help you search through it!")
    
    # Restaurant info
    restaurant_name = st.text_input("Restaurant Name")
    restaurant_location = st.text_input("Location/Address")
    restaurant_rating = st.slider("Restaurant Rating (1-5 stars)", 1.0, 5.0, 4.5, 0.1)
    
    # PDF upload
    uploaded_file = st.file_uploader("Upload Menu (PDF)", type=['pdf'])
    
    if uploaded_file and st.button("📤 Upload Menu", use_container_width=True):
        with st.spinner("Processing menu..."):
            # Save uploaded file
            with open(f"temp_{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Extract menu items
            menu_items = extract_menu_items(f"temp_{uploaded_file.name}")
            
            st.success(f"✅ Menu uploaded successfully!")
            st.info(f"Found {len(menu_items)} items in the menu")
            
            # Display menu items
            with st.expander("View Menu Items"):
                for i, item in enumerate(menu_items[:20], 1):
                    if item.strip():
                        st.write(f"{i}. {item}")
            
            # Store in database
            if restaurant_name:
                db.add_restaurant(restaurant_name, restaurant_location)
                st.session_state.restaurants[restaurant_name] = {
                    'items': menu_items,
                    'rating': restaurant_rating,
                    'location': restaurant_location
                }

# MY ORDERS PAGE
elif page == "📊 My Orders":
    st.header("📊 Order History")
    
    if st.session_state.chat_history:
        st.subheader("Your Search History:")
        for i, entry in enumerate(st.session_state.chat_history, 1):
            with st.expander(f"Search #{i}: {entry['user'][:50]}..."):
                st.write(entry['bot'])
    else:
        st.info("No searches yet. Start by using the Food Chatbot!")
    
    # Restaurant library
    if st.session_state.restaurants:
        st.divider()
        st.subheader("Saved Restaurants:")
        for restaurant, data in st.session_state.restaurants.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{restaurant}** - ⭐ {data['rating']}")
                st.caption(f"📍 {data['location']}")
            with col2:
                if st.button(f"View {restaurant.split()[0]}", key=restaurant):
                    st.write(f"{len(data['items'])} items available")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 14px;'>
    <p>GRAB Senior Helper v1.0 | Designed for Senior Citizens in Singapore</p>
    <p>For support, contact: support@grabseniorhelper.sg</p>
</div>
""", unsafe_allow_html=True)