import re

# Tone transformation word maps
CASUAL_REPLACEMENTS = {
    'however': 'but',
    'therefore': 'so',
    'consequently': 'as a result',
    'furthermore': 'also',
    'nevertheless': 'still',
    'demonstrate': 'show',
    'utilize': 'use',
    'facilitate': 'help',
    'implement': 'set up',
    'significant': 'big',
    'substantial': 'huge',
    'approximately': 'about',
    'individuals': 'people',
    'numerous': 'many',
    'achieve': 'get',
    'regarding': 'about',
    'obtain': 'get',
    'require': 'need',
}

PROFESSIONAL_REPLACEMENTS = {
    'use': 'utilize',
    'help': 'facilitate',
    'get': 'obtain',
    'show': 'demonstrate',
    'big': 'significant',
    'many': 'numerous',
    'need': 'require',
    'about': 'regarding',
}

EDUCATIONAL_PREFIXES = [
    "Let's explore this concept: ",
    "Here's what you need to know: ",
    "Understanding this is key: ",
    "An important insight: ",
]

CASUAL_INTROS = [
    "Here's the thing — ",
    "So basically, ",
    "Here's what's cool: ",
    "Quick insight: ",
]

PROFESSIONAL_INTROS = [
    "Key insight: ",
    "Important observation: ",
    "Notable finding: ",
    "Critical point: ",
]

def apply_tone(text, tone):
    """Apply tone transformation to text."""
    if not text:
        return text
    
    if tone == 'casual':
        for formal, casual in CASUAL_REPLACEMENTS.items():
            text = re.sub(r'\b' + formal + r'\b', casual, text, flags=re.IGNORECASE)
        return text
    
    elif tone == 'professional':
        for casual, formal in PROFESSIONAL_REPLACEMENTS.items():
            text = re.sub(r'\b' + casual + r'\b', formal, text, flags=re.IGNORECASE)
        return text
    
    elif tone == 'educational':
        # Add clarifying language
        text = re.sub(r'\. ', '. This means that ', text, count=1)
        return text
    
    return text

def get_tone_hook(tone):
    """Get an engaging opening hook based on tone."""
    hooks = {
        'professional': [
            "Here's a key insight from today's content.",
            "This concept is transforming how professionals work.",
            "A critical idea worth understanding.",
        ],
        'casual': [
            "This is something you NEED to know! 🔥",
            "Nobody talks about this enough...",
            "Wait — did you know this? 👀",
            "Here's something that'll blow your mind! 💡",
        ],
        'educational': [
            "Let's break this down step by step.",
            "Here's a concept every learner should understand.",
            "Learning this changed how I think about it.",
            "Let's dive into this important topic.",
        ],
    }
    import random
    return random.choice(hooks.get(tone, hooks['professional']))

def get_tone_cta(tone):
    """Get a call-to-action based on tone."""
    ctas = {
        'professional': "Follow for more insights and professional content.",
        'casual': "Drop a 🔥 if this helped! Follow for more!",
        'educational': "Save this for later! More learning content coming soon.",
    }
    return ctas.get(tone, ctas['professional'])

def get_tone_emoji(tone):
    """Get emoji set for tone."""
    emojis = {
        'professional': ['💼', '📊', '✅', '🎯', '💡'],
        'casual': ['🔥', '💥', '👀', '✨', '🚀'],
        'educational': ['📚', '💡', '🧠', '✏️', '🎓'],
    }
    return emojis.get(tone, emojis['professional'])
