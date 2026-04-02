from nlp.text_cleaner import tokenize_sentences, clean_text
from nlp.keyword_extractor import extract_keywords

MAX_TWEET_LEN = 270  # leave room for numbering


def split_into_thread(text, tone='professional', add_hook=True, add_cta=True):
    """Split long-form content into a numbered Twitter/X thread."""
    text = clean_text(text)
    sentences = tokenize_sentences(text)
    keywords = extract_keywords(text, top_n=4)
    hashtags = ' '.join('#' + ''.join(w.capitalize() for w in kw.split()) for kw in keywords[:3])

    tweets = []
    current = ''

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        candidate = (current + ' ' + sentence).strip()
        if len(candidate) <= MAX_TWEET_LEN:
            current = candidate
        else:
            if current:
                tweets.append(current.strip())
            if len(sentence) > MAX_TWEET_LEN:
                words = sentence.split()
                chunk = ''
                for word in words:
                    if len(chunk + ' ' + word) <= MAX_TWEET_LEN:
                        chunk = (chunk + ' ' + word).strip()
                    else:
                        if chunk:
                            tweets.append(chunk)
                        chunk = word
                if chunk:
                    current = chunk
            else:
                current = sentence

    if current:
        tweets.append(current.strip())

    if not tweets:
        return ["Not enough content to create a thread."]

    thread = []

    if add_hook and tweets:
        thread.append(f"🧵 THREAD: {tweets[0]}\n\n{hashtags}")
        body_tweets = tweets[1:]
    else:
        body_tweets = tweets

    total = len(body_tweets) + (1 if add_cta else 0) + (1 if add_hook else 0)
    for i, tweet in enumerate(body_tweets, start=2 if add_hook else 1):
        thread.append(f"{i}/{total} {tweet}")

    if add_cta:
        cta_num = len(thread) + 1
        thread.append(
            f"{cta_num}/{cta_num} 💡 Found this useful? "
            f"Retweet the first tweet to share with your network.\n\nFollow for more threads like this! {hashtags}"
        )

    return thread


def format_thread_preview(thread):
    """Format thread as a single readable string."""
    return '\n\n---\n\n'.join(thread)
