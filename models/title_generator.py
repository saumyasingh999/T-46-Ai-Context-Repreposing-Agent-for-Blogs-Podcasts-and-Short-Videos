from nlp.text_cleaner import tokenize_sentences, clean_text
from nlp.keyword_extractor import extract_keywords
import random

LISTICLE_TEMPLATES = [
    "{n} Ways to {action} {topic}",
    "{n} Things You Need to Know About {topic}",
    "{n} Proven Strategies for {topic}",
    "{n} Secrets of {topic} That Nobody Tells You",
    "{n} Tips to Master {topic}",
]

HOW_TO_TEMPLATES = [
    "How to {action} {topic} (Step-by-Step Guide)",
    "How to Master {topic} in {n} Simple Steps",
    "The Ultimate Guide to {topic}",
    "A Beginner's Guide to {topic}",
    "How {topic} Can Transform Your Results",
]

QUESTION_TEMPLATES = [
    "Is {topic} Worth It? Here's What You Need to Know",
    "What Is {topic} and Why Does It Matter?",
    "Why {topic} Is the Future of {field}",
    "Are You Making These {topic} Mistakes?",
]

POWER_TEMPLATES = [
    "The Truth About {topic} Nobody Talks About",
    "Why Most People Fail at {topic} (And How to Succeed)",
    "The Complete {topic} Playbook",
    "Stop Ignoring {topic}: Here's Why It Matters",
    "Mastering {topic}: From Zero to Expert",
]

SEO_TEMPLATES = [
    "{topic}: Everything You Need to Know in {year}",
    "Best {topic} Strategies for {year}",
    "{topic} Guide: Tips, Tricks & Best Practices",
    "Complete {topic} Tutorial for Beginners",
]


def generate_titles(text, count=10):
    """Generate multiple title options from content."""
    keywords = extract_keywords(text, top_n=6)
    sentences = tokenize_sentences(clean_text(text))

    if not keywords:
        return ["Content Title — Add more text for better results"]

    topic = keywords[0].title() if keywords else "This Topic"
    field = keywords[1].title() if len(keywords) > 1 else "Your Industry"

    action_words = ['improve', 'grow', 'build', 'create', 'master', 'optimize', 'leverage', 'use']
    action = 'Improve'
    for word in action_words:
        if word in text.lower():
            action = word.capitalize()
            break

    n = random.choice([5, 7, 10, 3])
    year = 2025
    titles = []

    for tmpl in random.sample(LISTICLE_TEMPLATES, min(2, len(LISTICLE_TEMPLATES))):
        titles.append(tmpl.format(n=n, action=action, topic=topic))
    for tmpl in random.sample(HOW_TO_TEMPLATES, min(2, len(HOW_TO_TEMPLATES))):
        titles.append(tmpl.format(action=action, topic=topic, n=n))
    for tmpl in random.sample(QUESTION_TEMPLATES, min(2, len(QUESTION_TEMPLATES))):
        titles.append(tmpl.format(topic=topic, field=field))
    for tmpl in random.sample(POWER_TEMPLATES, min(2, len(POWER_TEMPLATES))):
        titles.append(tmpl.format(topic=topic))
    for tmpl in random.sample(SEO_TEMPLATES, min(2, len(SEO_TEMPLATES))):
        titles.append(tmpl.format(topic=topic, year=year))

    if sentences:
        titles.append(sentences[0][:80].rstrip('.,;:'))

    return titles[:count]
