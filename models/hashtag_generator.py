from nlp.keyword_extractor import extract_keywords
from nlp.text_cleaner import clean_text

def generate_hashtags(text, keywords=None, count=20):
    """Generate platform-optimized hashtags from text."""
    if not keywords:
        keywords = extract_keywords(text, top_n=count)

    hashtags = []
    seen = set()

    for kw in keywords:
        tag = '#' + ''.join(w.capitalize() for w in kw.split())
        if tag.lower() not in seen:
            hashtags.append(tag)
            seen.add(tag.lower())

    generic = ['#ContentCreator', '#DigitalMarketing', '#SocialMedia',
               '#ContentStrategy', '#Marketing', '#Growth']
    for g in generic:
        if g.lower() not in seen and len(hashtags) < count:
            hashtags.append(g)
            seen.add(g.lower())

    return hashtags[:count]


def hashtags_by_platform(text, keywords=None):
    """Return platform-specific hashtag sets."""
    all_tags = generate_hashtags(text, keywords, count=25)
    return {
        'instagram': ' '.join(all_tags[:20]),
        'twitter':   ' '.join(all_tags[:5]),
        'linkedin':  ' '.join(all_tags[:5]),
        'youtube':   ' '.join(all_tags[:15]),
        'tiktok':    ' '.join(all_tags[:8]),
    }
