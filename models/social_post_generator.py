from models.tone_controller import get_tone_emoji, apply_tone
from nlp.keyword_extractor import keywords_to_hashtags
from nlp.text_cleaner import tokenize_sentences
import random

def generate_social_posts(summary, highlights, keywords, tone='professional'):
    """
    Generate social media posts for multiple platforms.
    Returns dict with Twitter/X, Instagram, LinkedIn posts.
    """
    emojis = get_tone_emoji(tone)
    hashtags = keywords_to_hashtags(keywords)
    
    # Get best lines
    sentences = tokenize_sentences(summary)
    best_line = sentences[0] if sentences else summary[:150]
    best_line = apply_tone(best_line, tone)
    
    quote = highlights[0] if highlights else best_line
    quote = apply_tone(quote, tone)
    
    second_point = highlights[1] if len(highlights) > 1 else best_line
    second_point = apply_tone(second_point, tone)
    
    hashtag_str = ' '.join(hashtags[:4]) if hashtags else '#Content #Ideas'
    
    posts = {}
    
    # ── Twitter / X ──
    if tone == 'casual':
        posts['twitter'] = f"""{emojis[0]} Hot take:

"{quote[:180]}"

{hashtag_str}"""
    elif tone == 'educational':
        posts['twitter'] = f"""{emojis[0]} Quick lesson:

"{quote[:180]}"

Save this! {hashtag_str}"""
    else:
        posts['twitter'] = f"""{emojis[0]} Key insight:

"{quote[:180]}"

{hashtag_str}"""

    # ── Instagram ──
    bullet1 = highlights[0][:100] if highlights else best_line[:100]
    bullet2 = highlights[1][:100] if len(highlights) > 1 else second_point[:100]
    bullet3 = highlights[2][:100] if len(highlights) > 2 else best_line[:100]
    
    if tone == 'casual':
        posts['instagram'] = f"""{emojis[0]} This is worth saving!

{quote[:200]}

Here's what you need to know 👇
{emojis[1]} {apply_tone(bullet1, tone)}
{emojis[2]} {apply_tone(bullet2, tone)}
{emojis[3]} {apply_tone(bullet3, tone)}

Double tap if this helped! ❤️
{hashtag_str} #Viral #MustRead"""

    elif tone == 'educational':
        posts['instagram'] = f"""{emojis[0]} Learning moment!

{quote[:200]}

Key takeaways 👇
{emojis[1]} {apply_tone(bullet1, tone)}
{emojis[2]} {apply_tone(bullet2, tone)}
{emojis[3]} {apply_tone(bullet3, tone)}

Save this for your studies! 📌
{hashtag_str} #Learning #Education"""

    else:
        posts['instagram'] = f"""{emojis[0]} Professional insight:

{quote[:200]}

Key points 👇
{emojis[1]} {apply_tone(bullet1, tone)}
{emojis[2]} {apply_tone(bullet2, tone)}
{emojis[3]} {apply_tone(bullet3, tone)}

Follow for more professional content.
{hashtag_str}"""

    # ── LinkedIn ──
    full_summary = apply_tone(summary[:400], tone)
    
    if tone == 'casual':
        posts['linkedin'] = f"""Something I've been thinking about lately...

{full_summary}

Here are the key takeaways:
→ {apply_tone(bullet1, tone)}
→ {apply_tone(bullet2, tone)}
→ {apply_tone(bullet3, tone)}

What do you think? Drop your thoughts below 👇

{hashtag_str}"""

    elif tone == 'educational':
        posts['linkedin'] = f"""📚 Here's something important to understand:

{full_summary}

Key learnings:
→ {apply_tone(bullet1, tone)}
→ {apply_tone(bullet2, tone)}
→ {apply_tone(bullet3, tone)}

What's been your experience with this topic?

{hashtag_str} #ProfessionalDevelopment"""

    else:
        posts['linkedin'] = f"""💼 Professional insight worth sharing:

{full_summary}

Key observations:
→ {apply_tone(bullet1, tone)}
→ {apply_tone(bullet2, tone)}
→ {apply_tone(bullet3, tone)}

I'd love to hear your perspective. What are your thoughts?

{hashtag_str} #Leadership #Innovation"""

    return posts
