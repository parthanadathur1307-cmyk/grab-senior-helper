# Senior Helper App - GrabFood Assistant for Senior Citizens

A user-friendly Streamlit application designed to help senior citizens in Singapore easily order food from GrabFood with simplified interface, large fonts, and AI-powered assistance.

## Features

### 1. **Easy Restaurant Discovery**
- Browse restaurants by cuisine type
- Filter by price range
- View ratings and reviews
- Large, readable text and buttons

### 2. **Smart Menu Navigation**
- PDF menu upload and parsing
- AI-powered search within menus
- Dietary restrictions support
- Clear dish descriptions and prices

### 3. **Multilingual Support**
- English
- Simplified Chinese (简体中文)
- Malay (Bahasa Melayu)
- Tamil (தமிழ்)

### 4. **AI-Powered Chatbot**
- Personalized restaurant recommendations
- Dietary preference handling
- Budget-conscious suggestions
- Real-time dish search

### 5. **Senior-Friendly Interface**
- Large font sizes (20pt default)
- High contrast dark theme
- Simple navigation
- Clear call-to-action buttons
- Voice input support (coming soon)

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **Database**: SQLite
- **AI**: Google Gemini API
- **PDF Processing**: pdfplumber, pytesseract, pdf2image

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Tesseract OCR (for PDF menu scanning)

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/parthanadathur1307-cmyk/grab-senior-helper.git
cd grab-senior-helper
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```
GOOGLE_API_KEY=your_google_api_key_here
```

5. **Install Tesseract OCR**
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`
- **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki

6. **Run the application**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Usage Guide

### For Senior Citizens

1. **Start the App**: Click the large "Start" button on the home page
2. **Select Language**: Choose your preferred language
3. **Browse Restaurants**: 
   - View restaurants by cuisine
   - Click on a restaurant to see menu
4. **Order Food**:
   - Select dishes you want
   - Review your order
   - Place order through GrabFood

### For Caregivers/Family

1. Set dietary preferences for the senior
2. Set budget limits
3. Monitor order history
4. Configure emergency contacts

## Project Structure

```
grab-senior-helper/
├── app.py                 # Main Streamlit application
├── menu_parser.py         # PDF menu parsing and OCR
├── database.py            # SQLite database management
├── ai_chatbot.py          # Google Gemini AI integration
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── data/
    └── restaurants.db    # SQLite database (auto-created)
```

## Configuration

### Streamlit Config (.streamlit/config.toml)

```toml
[theme]
base = "dark"
primaryColor = "#FF5733"
fontSize = "20pt"
fontFamily = "Arial"

[server]
headless = true
enableCORS = false
port = 8501
```

## API Keys

### Google Gemini API
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Add to `.env` file as `GOOGLE_API_KEY`

## Database Schema

### Tables

**restaurants**
- id (PRIMARY KEY)
- name (TEXT)
- location (TEXT)

**menus**
- id (PRIMARY KEY)
- restaurant_id (FOREIGN KEY)
- name (TEXT)

**dishes**
- id (PRIMARY KEY)
- menu_id (FOREIGN KEY)
- name (TEXT)
- price (REAL)

## Supported Languages

| Language | Code | Support Level |
|----------|------|---|
| English | en | Full |
| Simplified Chinese | zh | Full |
| Malay | ms | Full |
| Tamil | ta | Full |

## Accessibility Features

- ✅ Large default font size (20pt)
- ✅ High contrast dark theme
- ✅ Simple, intuitive navigation
- ✅ Voice input support (beta)
- ✅ Text-to-speech for menu items (coming soon)
- ✅ Keyboard navigation support

## Troubleshooting

### "Tesseract not found"
Install Tesseract OCR following the installation instructions above.

### "API key invalid"
Check your `.env` file and ensure `GOOGLE_API_KEY` is correctly set.

### "Database locked"
Close all other instances of the app and try again.

### Slow menu parsing
For large PDFs, OCR processing may take time. Consider splitting large menus.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit with clear messages (`git commit -m 'Add feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Open a Pull Request

## Future Enhancements

- [ ] Voice input and output support
- [ ] Integration with actual GrabFood API
- [ ] Order history and favorites
- [ ] Loyalty rewards tracking
- [ ] Real-time delivery tracking
- [ ] Payment integration
- [ ] Mobile app version
- [ ] Offline mode support
- [ ] Family sharing features

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Email: parthanadathur1307@gmail.com

## Acknowledgments

- Google Gemini API for AI capabilities
- Streamlit for the excellent UI framework
- GrabFood for inspiring this helper app
- Special thanks to all testers and feedback contributors

---

**Made with ❤️ for senior citizens in Singapore**
