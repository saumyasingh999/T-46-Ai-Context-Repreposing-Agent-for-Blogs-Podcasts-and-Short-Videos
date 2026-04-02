from nlp.text_cleaner import tokenize_sentences, clean_text
from nlp.keyword_extractor import extract_keywords
from models.tone_controller import apply_tone


def convert_blog_to_linkedin(text, summary, highlights, keywords, tone='professional'):
    """
    Convert blog content into a LinkedIn-optimized long-form post.
    Short paragraphs, strong hook, bullet points, professional CTA, 3-5 hashtags.
    """
    sentences = tokenize_sentences(clean_text(text))
    hashtags = ' '.join('#' + ''.join(w.capitalize() for w in kw.split()) for kw in keywords[:5])

    hook_sentence = sentences[0] if sentences else summary[:120]
    hook = apply_tone(hook_sentence, tone)

    if tone == 'casual':
        opener = f"Here's something most people overlook 👇\n\n{hook}"
    elif tone == 'educational':
        opener = f"📚 Lesson of the day:\n\n{hook}"
    else:
        opener = f"An insight worth sharing:\n\n{hook}"

    body_points = []
    for h in highlights[:4]:
        body_points.append(f"→ {apply_tone(h[:200], tone)}")
    body = '\n\n'.join(body_points)

    mid_sentences = sentences[1:3] if len(sentences) > 2 else []
    insight = ' '.join(mid_sentences)
    insight_block = f"\nHere's what this means in practice:\n\n{apply_tone(insight, tone)}\n" if insight else ''

    if tone == 'casual':
        cta = "What do you think? Drop your thoughts below 👇\n\nAnd if this resonated, share it with someone who needs to see it."
    elif tone == 'educational':
        cta = "What's your experience with this? I'd love to hear your perspective in the comments.\n\nShare this if you found it valuable."
    else:
        cta = "I'd welcome your thoughts on this. What has your experience been?\n\nFeel free to share this with your network if it adds value."

    post = f"""{opener}

━━━━━━━━━━━━━━━━━━━━━━

{body}
{insight_block}
━━━━━━━━━━━━━━━━━━━━━━

{cta}

{hashtags}"""

    return post.strip()
