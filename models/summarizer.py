from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from nlp.text_cleaner import clean_text, tokenize_sentences
import re

def summarize_text(text, num_sentences=4):
    """
    Extractive summarization using TF-IDF sentence scoring.
    Lightweight — works on 8GB RAM without any GPU.
    """
    text = clean_text(text)
    sentences = tokenize_sentences(text)
    
    if not sentences:
        return "Could not generate summary."
    
    if len(sentences) <= num_sentences:
        return ' '.join(sentences)
    
    try:
        # TF-IDF vectorization — no stop words for multilingual support
        vectorizer = TfidfVectorizer(stop_words=None)
        tfidf_matrix = vectorizer.fit_transform(sentences)
        
        # Score sentences by their TF-IDF sum
        scores = np.array(tfidf_matrix.sum(axis=1)).flatten()
        
        # Boost first and last sentences (they tend to be important)
        scores[0] *= 1.5
        if len(scores) > 1:
            scores[-1] *= 1.2
        
        # Get top N sentence indices (keep original order)
        top_indices = sorted(
            np.argsort(scores)[-num_sentences:].tolist()
        )
        
        summary = ' '.join([sentences[i] for i in top_indices])
        return summary
    
    except Exception as e:
        # Fallback: first few sentences
        return ' '.join(sentences[:num_sentences])

def chunk_and_summarize(text, chunk_size=500, num_sentences=4):
    """
    For very long texts: chunk → summarize each → merge.
    Prevents memory issues on low-end hardware.
    """
    words = text.split()
    
    if len(words) <= chunk_size:
        return summarize_text(text, num_sentences)
    
    # Split into chunks
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    # Summarize each chunk
    chunk_summaries = []
    for chunk in chunks:
        s = summarize_text(chunk, num_sentences=2)
        chunk_summaries.append(s)
    
    # Merge and summarize again
    merged = ' '.join(chunk_summaries)
    return summarize_text(merged, num_sentences)
