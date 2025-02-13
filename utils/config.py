import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

AVAILABLE_MODELS = [
    'gemini-1.0-pro',
    'gemini-1.5-flash',
    'gemini-1.5-flash-8b',
    'gemini-1.5-flash-8b-exp',
    'gemini-1.5-flash-exp',
    'gemini-1.5-pro',
    'gemini-1.5-pro-exp',
    'gemini-2.0-flash-exp'
]

EXPERTISE_LEVELS = [
    'storyteller',
    'novelist',
    'journalist',
    'poet',
    'screenwriter',
    'critic',
    'researcher',  # Added for academic topics
    'educator',    # Added for educational content
    'analyst'      # Added for technical/business topics
]

TONE_STYLES = [
    'funny',
    'serious',
    'dramatic',
    'sarcastic',
    'critical',
    'mysterious',
    'emotional',
    'neutral',
    'educational', # Added for learning content
    'technical',   # Added for complex topics
    'casual'       # Added for conversational style
]

# New: Topic Categories for better content organization
TOPIC_CATEGORIES = {
    'technology': {
        'subcategories': ['software', 'hardware', 'ai', 'cybersecurity', 'internet', 'gadgets'],
        'keywords': ['tech', 'digital', 'innovation', 'computing', 'electronic']
    },
    'science': {
        'subcategories': ['physics', 'biology', 'chemistry', 'astronomy', 'environment'],
        'keywords': ['research', 'discovery', 'experiment', 'scientific', 'study']
    },
    'business': {
        'subcategories': ['entrepreneurship', 'marketing', 'finance', 'management', 'startups'],
        'keywords': ['market', 'company', 'industry', 'economic', 'commercial']
    },
    'arts': {
        'subcategories': ['visual-arts', 'music', 'literature', 'theater', 'film'],
        'keywords': ['creative', 'artistic', 'cultural', 'aesthetic', 'design']
    },
    'lifestyle': {
        'subcategories': ['health', 'fitness', 'food', 'travel', 'fashion'],
        'keywords': ['wellness', 'lifestyle', 'living', 'personal', 'daily']
    },
    'education': {
        'subcategories': ['learning', 'teaching', 'academic', 'skills', 'training'],
        'keywords': ['educational', 'learning', 'academic', 'study', 'knowledge']
    },
    'current_events': {
        'subcategories': ['politics', 'society', 'economy', 'environment', 'culture'],
        'keywords': ['news', 'current', 'trending', 'contemporary', 'events']
    }
}

def init_gemini(model_name='gemini-2.0-flash-exp', api_key=None):
    if model_name not in AVAILABLE_MODELS:
        raise ValueError(f"Model {model_name} not supported")
    
    if not api_key:
        api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        raise ValueError("API key not found")
        
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)

def get_topic_category(topic: str) -> str:
    """
    Determine the most likely category for a given topic based on keywords
    """
    topic_lower = topic.lower()
    
    for category, data in TOPIC_CATEGORIES.items():
        # Check keywords
        if any(keyword in topic_lower for keyword in data['keywords']):
            return category
        # Check subcategories
        if any(subcat in topic_lower for subcat in data['subcategories']):
            return category
    
    return 'general'  # Default category if no match found