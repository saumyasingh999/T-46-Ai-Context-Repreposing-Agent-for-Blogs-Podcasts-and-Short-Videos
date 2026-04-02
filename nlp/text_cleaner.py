import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download required NLTK data
def ensure_nltk_data():
    resources = ['punkt', 'stopwords', 'averaged_perceptron_tagger', 'punkt_tab']
    for r in resources:
        try:
            nltk.download(r, quiet=True)
        except Exception:
            pass

ensure_nltk_data()

def clean_text(text):
    """Full text cleaning pipeline."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize_sentences(text):
    """Split text into clean sentences."""
    text = clean_text(text)
    sentences = sent_tokenize(text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    return sentences

def remove_stopwords(text):
    """Remove stopwords for keyword extraction."""
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words and len(t) > 2]
    return tokens

def preprocess_for_model(text):
    """Prepare text for NLP processing."""
    text = clean_text(text)
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?]', '', text)
    return text
