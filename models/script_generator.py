from models.tone_controller import get_tone_hook, get_tone_cta, apply_tone
from nlp.text_cleaner import tokenize_sentences

def generate_script(summary, highlights, tone='professional'):
    """
    Generate a 30–60 second short video script.
    Structure: Hook → Context → Main Idea → Example → CTA
    """
    hook = get_tone_hook(tone)
    cta = get_tone_cta(tone)
    
    # Shorten summary to ~2 sentences
    sentences = tokenize_sentences(summary)
    main_idea = ' '.join(sentences[:2]) if sentences else summary
    main_idea = apply_tone(main_idea, tone)
    
    # Pick an example from highlights
    example = ""
    if highlights and len(highlights) > 1:
        example = highlights[1]
        example = apply_tone(example, tone)
    
    # Build script based on tone style
    if tone == 'casual':
        script = f"""🎬 VIDEO SCRIPT (30–60 seconds)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[HOOK — 0:00–0:05]
{hook}

[CONTEXT — 0:05–0:15]
Most people don't realize this, but it matters more than you think.

[MAIN IDEA — 0:15–0:35]
{main_idea}

[EXAMPLE — 0:35–0:50]
{example if example else "Think about it — small changes add up over time."}

[CALL TO ACTION — 0:50–0:60]
{cta}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱ Estimated Duration: ~45 seconds"""

    elif tone == 'educational':
        script = f"""🎬 VIDEO SCRIPT (30–60 seconds)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[HOOK — 0:00–0:05]
{hook}

[LEARNING OBJECTIVE — 0:05–0:15]
By the end of this, you'll understand the core concept clearly.

[EXPLANATION — 0:15–0:40]
{main_idea}

[EXAMPLE / APPLICATION — 0:40–0:55]
{example if example else "Let's look at how this applies in a real-world scenario."}

[SUMMARY & CTA — 0:55–1:00]
{cta}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱ Estimated Duration: ~60 seconds"""

    else:  # professional
        script = f"""🎬 VIDEO SCRIPT (30–60 seconds)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[HOOK — 0:00–0:05]
{hook}

[CONTEXT — 0:05–0:15]
This is something every professional should be aware of.

[KEY MESSAGE — 0:15–0:40]
{main_idea}

[SUPPORTING POINT — 0:40–0:55]
{example if example else "The data consistently supports this conclusion."}

[CALL TO ACTION — 0:55–1:00]
{cta}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱ Estimated Duration: ~55 seconds"""
    
    return script

def generate_reel_idea(highlights, tone='professional'):
    """Generate a short reel concept from highlights."""
    if not highlights:
        return "No reel idea generated."
    
    best = highlights[0]
    hook = get_tone_hook(tone)
    cta = get_tone_cta(tone)
    
    return f"""💡 REEL CONCEPT
Hook: {hook}
Quote on screen: "{best}"
Voiceover: "{apply_tone(best, tone)}"
End screen: {cta}"""
