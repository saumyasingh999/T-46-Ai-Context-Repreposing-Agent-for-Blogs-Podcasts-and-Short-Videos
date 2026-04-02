from sklearn.feature_extraction.text import TfidfVectorizer
from nlp.text_cleaner import clean_text, remove_stopwords
import re

def extract_keywords(text, top_n=8):
    """Extract top keywords using TF-IDF."""
    text = clean_text(text)
    
    # Split into chunks for TF-IDF
    sentences = re.split(r'[.!?]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    if len(sentences) < 2:
        # Fallback: frequency-based
        tokens = remove_stopwords(text)
        freq = {}
        for t in tokens:
            freq[t] = freq.get(t, 0) + 1
        sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [w for w, _ in sorted_words[:top_n]]
    
    try:
        vectorizer = TfidfVectorizer(
            max_features=50,
            stop_words='english',
            ngram_range=(1, 2)
        )
        X = vectorizer.fit_transform(sentences)
        
        # Sum TF-IDF scores across all sentences
        scores = X.sum(axis=0).A1
        feature_names = vectorizer.get_feature_names_out()
        
        ranked = sorted(
            zip(scores, feature_names),
            reverse=True
        )
        
        keywords = [kw for _, kw in ranked[:top_n]]
        return keywords
    except Exception:
        tokens = remove_stopwords(text)
        freq = {}
        for t in tokens:
            freq[t] = freq.get(t, 0) + 1
        sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [w for w, _ in sorted_words[:top_n]]

def keywords_to_hashtags(keywords):
    """Convert keywords to hashtags."""
    hashtags = []
    for kw in keywords[:5]:
        tag = '#' + ''.join(w.capitalize() for w in kw.split())
        hashtags.append(tag)
    return hashtags
