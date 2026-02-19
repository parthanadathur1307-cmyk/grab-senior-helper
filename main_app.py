import streamlit as st
import google.generativeai as genai
from menu_parser import extract_menu_items, extract_menu_items_with_ocr
from database import Database
import json

# Initialize session state
if 'api_key_configured' not in st.session_state:
    st.session_state.api_key_configured = False

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'selected_language' not in st.session_state:
    st.session_state.selected_language = 'English'

# Page configuration
st.set_page_config(page_title="GRAB Senior Helper", layout="wide")

# Language translations
TRANSLATIONS = {
    'English': {
        'title': 'GRAB Senior Helper - Find Food & Restaurants',
        'language': 'Language',
        'api_key': 'Enter Google API Key',
        'upload_menu': 'Upload Restaurant Menu (PDF)',
        'dietary': 'Dietary Restrictions',
        'price_range': 'Price Range',
        'search': 'Search',
        'chat': 'Chat with Assistant',
        'results': 'Search Results'
    },
    'Chinese': {
        'title': 'GRAB 老年人助手 - 查找食物和餐厅',
        'language': '语言',
        'api_key': '输入 Google API 密钥',
        'upload_menu': '上传餐厅菜单 (PDF)',
        'dietary': '饮食限制',
        'price_range': '价格范围',
        'search': '搜索',
        'chat': '与助手聊天',
        'results': '搜索结果'
    },
    'Malay': {
        'title': 'GRAB Pembantu Warga Tua - Cari Makanan & Restoran',
        'language': 'Bahasa',
        'api_key': 'Masukkan Kunci API Google',
        'upload_menu': 'Muat Naik Menu Restoran (PDF)',
        'dietary': 'Sekatan Pemakanan',
        'price_range': 'Julat Harga',
        'search': 'Cari',
        'chat': 'Berbual dengan Pembantu',
        'results': 'Hasil Carian'
    },
    'Tamil': {
        'title': 'GRAB மூத்த குடிமக்கள் உதவி - உணவு மற்றும் உணவகங்களைத் தேடுங்கள்',
        'language': 'மொழி',
        'api_key': 'Google API விசையை உள்ளிடவும்',
        'upload_menu': 'உணவகத்தின் மெனு பதிவேற்றவும் (PDF)',
        'dietary': 'உணவு கட்டுப்பாடுகள்',
        'price_range': 'விலை வரம்பு',
        'search': 'தேடு',
        'chat': 'உதவியாளருடன் சேவையளிக்கவும்',
        'results': 'தேடல் முடிவுகள்'
    }
}

def get_text(key):
    """Get translated text based on selected language"""
    lang = st.session_state.selected_language
    return TRANSLATIONS[lang].get(key, TRANSLATIONS['English'].get(key, key))

def configure_gemini(api_key):
    """Configure Google Gemini API"""
    genai.configure(api_key=api_key)
    st.session_state.api_key_configured = True
    st.success("API Key configured successfully!")

def search_with_ai(user_query, dietary_restrictions, price_range, menu_data):
    """Use Google Gemini to find best restaurants/dishes"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
You are a helpful assistant for senior citizens looking for food in Singapore via GRAB delivery.
Be clear, simple, and friendly.

User Query: {user_query}
Dietary Restrictions: {dietary_restrictions}
Price Range: {price_range}
Available Menu Items: {menu_data}

Please recommend suitable restaurants/dishes based on the criteria.
Consider dietary restrictions and price preferences.
Provide: Restaurant name, dish name, price, and why it's suitable.
"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Main UI
st.title(get_text('title'))

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Language selection
    st.session_state.selected_language = st.selectbox(
        get_text('language'),
        ['English', 'Chinese', 'Malay', 'Tamil']
    )
    
    # API Key input
    api_key = st.text_input(get_text('api_key'), type="password")
    if api_key:
        configure_gemini(api_key)
    
    st.divider()
    st.caption("Prototype for Singapore GRAB Food Delivery")

# Main content tabs
tab1, tab2, tab3 = st.tabs(["🍽️ Search Restaurants", "📄 Upload Menu", "💬 Chat Assistant"])

with tab1:
    st.header("Find Restaurants & Dishes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        dietary_restrictions = st.text_input(
            get_text('dietary'),
            placeholder="e.g., No pork, vegetarian, etc."
        )
    
    with col2:
        price_range = st.selectbox(
            get_text('price_range'),
            ["Any", "$", "$$", "$$$"]
        )
    
    search_query = st.text_input(
        "What would you like to eat?",
        placeholder="e.g., chicken rice, fish dishes, etc."
    )
    
    if st.button(get_text('search'), use_container_width=True):
        if not st.session_state.api_key_configured:
            st.error("Please configure API key first!")
        elif search_query:
            with st.spinner("Searching..."):
                result = search_with_ai(
                    search_query,
                    dietary_restrictions,
                    price_range,
                    "Sample menu data"
                )
                st.subheader(get_text('results'))
                st.write(result)

with tab2:
    st.header("Upload Restaurant Menu")
    
    uploaded_file = st.file_uploader(get_text('upload_menu'), type=['pdf'])
    
    if uploaded_file is not None:
        if st.button("Extract Menu Items"):
            try:
                with st.spinner("Processing PDF..."):
                    # Save uploaded file temporarily
                    with open('temp_menu.pdf', 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Try text extraction first, then OCR
                    menu_items = extract_menu_items('temp_menu.pdf')
                    if not menu_items or len(menu_items) < 5:
                        menu_items = extract_menu_items_with_ocr('temp_menu.pdf')
                    
                    st.success(f"Extracted {len(menu_items)} items!")
                    st.write("Sample items:")
                    for item in menu_items[:10]:
                        if item.strip():
                            st.write(f"• {item}")
            except Exception as e:
                st.error(f"Error processing menu: {str(e)}")

with tab3:
    st.header(get_text('chat'))
    
    # Chat history display
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Ask me anything...")
    
    if user_input:
        if not st.session_state.api_key_configured:
            st.error("Please configure API key first!")
        else:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            with st.chat_message("user"):
                st.write(user_input)
            
            with st.spinner("Thinking..."):
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(
                        f"You are a helpful assistant for senior citizens. Answer simply and clearly. User: {user_input}"
                    )
                    assistant_response = response.text
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": assistant_response
                    })
                    
                    with st.chat_message("assistant"):
                        st.write(assistant_response)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
