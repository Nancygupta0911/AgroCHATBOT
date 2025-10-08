# chatbot_model.py
import random

# Multilingual responses (English, Hindi, Tamil)
RESPONSES = {
    "greeting": {
        "en": [
            "Hello! I'm your agriculture assistant. 🌱 How can I help you today?",
            "Hi there! Ask me anything about farming and crops. 🚜"
        ],
        "hi": [
            "नमस्ते! मैं आपका कृषि सहायक हूँ। 🌱 मैं आपकी कैसे मदद कर सकता हूँ?",
            "हाय! खेती और फसलों के बारे में कुछ भी पूछ सकते हैं। 🚜"
        ],
        "ta": [
            "வணக்கம்! நான் உங்கள் வேளாண் உதவியாளர். 🌾 இன்று உங்களுக்கு என்ன உதவி வேண்டும்?",
            "ஹாய்! விவசாயம் மற்றும் பயிர்கள் குறித்து எதை வேண்டுமானாலும் கேளுங்கள். 🚜"
        ]
    },
    "fertilizer": {
        "en": [
            "For better yield, use organic compost and nitrogen-rich fertilizer like urea.",
            "Consider using phosphorus and potassium-based fertilizers for root growth."
        ],
        "hi": [
            "बेहतर उत्पादन के लिए, जैविक खाद और नाइट्रोजन युक्त उर्वरक जैसे यूरिया का उपयोग करें।",
            "जड़ विकास के लिए फॉस्फोरस और पोटैशियम आधारित उर्वरकों का उपयोग करें।"
        ],
        "ta": [
            "சிறந்த விளைச்சலுக்கு, இயற்கை உரம் மற்றும் யூரியா போன்ற நைட்ரஜன் நிறைந்த உரத்தை பயன்படுத்துங்கள்.",
            "வேர் வளர்ச்சிக்கு பாஸ்பரஸ் மற்றும் பொட்டாசியம் அடிப்படையிலான உரங்களை பயன்படுத்துங்கள்."
        ]
    },
    "pest": {
        "en": [
            "Neem oil spray is effective for many pests.",
            "Introduce natural predators like ladybugs to control pest population."
        ],
        "hi": [
            "नीम का तेल कई कीड़ों के लिए प्रभावी है।",
            "कीट आबादी को नियंत्रित करने के लिए प्राकृतिक शिकारी जैसे लेडीबग्स का परिचय दें।"
        ],
        "ta": [
            "வெப்பச்செடி எண்ணெய் தெளிப்பு பல பூச்சிகளுக்கு பயனுள்ளதாக இருக்கும்.",
            "லேடிபக்ஸ் போன்ற இயற்கை எதிரிகளை அறிமுகப்படுத்தி பூச்சிகளை கட்டுப்படுத்துங்கள்."
        ]
    },
    "weather": {
        "en": [
            "Please check the local forecast before sowing seeds.",
            "Avoid watering plants if heavy rain is predicted."
        ],
        "hi": [
            "बीज बोने से पहले स्थानीय मौसम पूर्वानुमान जांचें।",
            "यदि भारी बारिश की भविष्यवाणी है तो पौधों को पानी न दें।"
        ],
        "ta": [
            "விதைகள் விதைக்கும் முன் உள்ளூர் வானிலை முன்னறிவிப்பை சரிபார்க்கவும்.",
            "கனமழை எதிர்பார்க்கப்பட்டால் தாவரங்களுக்கு நீர் ஊற்றுவதை தவிர்க்கவும்."
        ]
    },
    "default": {
        "en": [
            "I'm not sure about that. Could you please rephrase?",
            "Sorry, I don't understand. Can you ask another question?"
        ],
        "hi": [
            "मुझे उसके बारे में निश्चित नहीं है। कृपया इसे दोबारा पूछें।",
            "माफ़ करें, मुझे समझ नहीं आया। क्या आप दूसरा सवाल पूछ सकते हैं?"
        ],
        "ta": [
            "அதைப் பற்றி எனக்கு உறுதி இல்லை. தயவு செய்து மீண்டும் விளக்கமாகக் கேளுங்கள்.",
            "மன்னிக்கவும், எனக்கு புரியவில்லை. வேறு கேள்வி கேளுங்கள்."
        ]
    }
}

# Keyword mapping (extend as needed)
KEYWORDS = {
    "greeting": {
        "en": ["hello", "hi", "hey"],
        "hi": ["नमस्ते", "हाय", "हेलो"],
        "ta": ["வணக்கம்", "ஹாய்"]
    },
    "fertilizer": {
        "en": ["fertilizer", "urea", "compost"],
        "hi": ["उर्वरक", "खाद", "यूरिया"],
        "ta": ["உரம்", "யூரியா", "நைட்ரஜன்"]
    },
    "pest": {
        "en": ["pest", "bug", "insect"],
        "hi": ["कीट"],
        "ta": ["பூச்சி"]
    },
    "weather": {
        "en": ["weather", "rain", "forecast"],
        "hi": ["मौसम", "बारिश", "पूर्वानुमान"],
        "ta": ["வானிலை", "மழை"]
    }
}


def detect_language(text: str) -> str:
    """
    Rudimentary language detection using keywords and Unicode ranges.
    Returns one of 'en', 'hi', 'ta' (defaults to 'en').
    """
    if not text:
        return "en"
    txt = text.lower()

    # check for explicit keywords per language
    for lang in ("en", "hi", "ta"):
        for kws in KEYWORDS.values():
            for kw in kws.get(lang, []):
                if kw in txt:
                    return lang

    # fallback: detect by unicode ranges
    for ch in txt:
        if "\u0900" <= ch <= "\u097F":  # Devanagari -> Hindi
            return "hi"
        if "\u0B80" <= ch <= "\u0BFF":  # Tamil
            return "ta"

    return "en"


def get_response(user_input: str) -> str:
    """
    Return a response in the same language as user_input.
    Safe for empty input and always returns a string.
    """
    if not user_input:
        return random.choice(RESPONSES["default"]["en"])

    lang = detect_language(user_input)
    text = user_input.lower()

    # category matching
    if any(k in text for k in KEYWORDS["greeting"].get(lang, [])):
        return random.choice(RESPONSES["greeting"][lang])
    if any(k in text for k in KEYWORDS["fertilizer"].get(lang, [])):
        return random.choice(RESPONSES["fertilizer"][lang])
    if any(k in text for k in KEYWORDS["pest"].get(lang, [])):
        return random.choice(RESPONSES["pest"][lang])
    if any(k in text for k in KEYWORDS["weather"].get(lang, [])):
        return random.choice(RESPONSES["weather"][lang])

    # fallback default in detected language
    return random.choice(RESPONSES["default"][lang])






