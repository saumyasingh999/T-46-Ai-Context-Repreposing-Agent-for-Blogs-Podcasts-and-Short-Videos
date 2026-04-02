from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from nlp.text_cleaner import clean_text, tokenize_sentences

def extract_highlights(text, num_highlights=5):
    """
    Extract the most impactful sentences as highlights/quotes.
    Uses TF-IDF scoring + length filtering.
    """
    text = clean_text(text)
    sentences = tokenize_sentences(text)
    
    if not sentences:
        return ["No highlights found."]
    
    if len(sentences) <= num_highlights:
        return sentences
    
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(sentences)
        
        scores = np.array(tfidf_matrix.sum(axis=1)).flatten()
        
        # Prefer medium-length sentences (not too short, not too long)
        length_scores = []
        for s in sentences:
            word_count = len(s.split())
            # Ideal highlight: 8–25 words
            if 8 <= word_count <= 25:
                length_scores.append(1.3)
            elif word_count < 8:
                length_scores.append(0.5)
            else:
                length_scores.append(0.9)
        
        combined_scores = scores * np.array(length_scores)
        
        # Get top N sentence indices
        top_indices = np.argsort(combined_scores)[-num_highlights:].tolist()
        top_indices.sort()  # Keep original order
        
        highlights = [sentences[i] for i in top_indices]
        return highlights
    
    except Exception:
        return sentences[:num_highlights]

def get_best_quote(text):
    """Get single best quote for social media."""
    highlights = extract_highlights(text, num_highlights=3)
    if highlights:
        # Pick the shortest impactful one
        return min(highlights, key=lambda s: len(s))
    return ""
