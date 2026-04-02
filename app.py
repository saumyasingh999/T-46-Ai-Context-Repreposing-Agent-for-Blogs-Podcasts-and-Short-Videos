from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from werkzeug.utils import secure_filename
from models.summarizer import chunk_and_summarize
from models.highlight_extractor import extract_highlights
from models.script_generator import generate_script, generate_reel_idea
from models.social_post_generator import generate_social_posts
from models.tone_controller import apply_tone
from models.hashtag_generator import generate_hashtags, hashtags_by_platform
from models.title_generator import generate_titles
from models.twitter_thread_splitter import split_into_thread, format_thread_preview
from models.blog_to_linkedin import convert_blog_to_linkedin
from nlp.text_cleaner import clean_text
from nlp.keyword_extractor import extract_keywords
from database.db import init_db, save_result, get_all_results, get_result_by_id
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)
os.makedirs('database', exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_AUDIO


def run_pipeline(text, tone):
    """Run the full AI pipeline on text and return all outputs."""
    summary       = chunk_and_summarize(text)
    highlights    = extract_highlights(text)
    keywords      = extract_keywords(text)
    summary_toned = apply_tone(summary, tone)
    script        = generate_script(summary_toned, highlights, tone)
    social_posts  = generate_social_posts(summary_toned, highlights, keywords, tone)
    reel_idea     = generate_reel_idea(highlights, tone)
    hashtags      = generate_hashtags(text, keywords)
    titles        = generate_titles(text)
    thread        = split_into_thread(summary_toned + ' ' + ' '.join(highlights), tone)
    linkedin_post = convert_blog_to_linkedin(text, summary_toned, highlights, keywords, tone)
    return dict(
        summary=summary_toned, highlights=highlights, keywords=keywords,
        script=script, social_posts=social_posts, reel_idea=reel_idea,
        hashtags=hashtags, titles=titles, twitter_thread=thread,
        linkedin_post=linkedin_post
    )


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        text = request.form.get('blog_text', '').strip()
        url  = request.form.get('blog_url', '').strip()
        tone = request.form.get('tone', 'professional')

        if url and not text:
            try:
                import requests as req
                from bs4 import BeautifulSoup
                headers = {'User-Agent': 'Mozilla/5.0'}
                r = req.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(r.text, 'html.parser')
                text = ' '.join(p.get_text() for p in soup.find_all('p'))
                text = clean_text(text)
            except Exception as e:
                flash(f'Could not fetch URL: {str(e)}', 'error')
                return render_template('blog.html')

        if not text or len(text) < 50:
            flash('Please provide at least 50 characters of content.', 'error')
            return render_template('blog.html')

        p = run_pipeline(text, tone)
        result_id = save_result(
            input_type='blog', input_text=text,
            summary=p['summary'], highlights=p['highlights'],
            script=p['script'], social_posts=p['social_posts'],
            keywords=p['keywords'], tone=tone,
            hashtags=p['hashtags'], titles=p['titles'],
            twitter_thread=p['twitter_thread'], linkedin_post=p['linkedin_post']
        )
        return redirect(url_for('result', result_id=result_id))

    return render_template('blog.html')


@app.route('/podcast', methods=['GET', 'POST'])
def podcast():
    if request.method == 'POST':
        tone = request.form.get('tone', 'professional')
        language = request.form.get('language', 'auto')

        if 'audio_file' not in request.files:
            flash('Please select an audio file.', 'error')
            return render_template('podcast.html')

        file = request.files['audio_file']
        if file.filename == '':
            flash('No file selected.', 'error')
            return render_template('podcast.html')

        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload WAV, MP3, OGG, or M4A.', 'error')
            return render_template('podcast.html')

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            from speech.transcriber import transcribe_audio
            transcript = transcribe_audio(filepath, language=language)

            if not transcript or len(transcript.strip()) < 20:
                flash('Transcription failed or produced insufficient text.', 'error')
                return render_template('podcast.html')

            p = run_pipeline(transcript, tone)
            result_id = save_result(
                input_type='podcast', input_text=transcript,
                summary=p['summary'], highlights=p['highlights'],
                script=p['script'], social_posts=p['social_posts'],
                keywords=p['keywords'], tone=tone,
                hashtags=p['hashtags'], titles=p['titles'],
                twitter_thread=p['twitter_thread'], linkedin_post=p['linkedin_post']
            )
            return redirect(url_for('result', result_id=result_id))

        except Exception as e:
            flash(f'Processing error: {str(e)}', 'error')
            return render_template('podcast.html')

    return render_template('podcast.html')


@app.route('/youtube', methods=['GET', 'POST'])
def youtube():
    if request.method == 'POST':
        yt_url = request.form.get('yt_url', '').strip()
        tone   = request.form.get('tone', 'professional')
        language = request.form.get('language', 'auto')

        if not yt_url:
            flash('Please enter a YouTube URL.', 'error')
            return render_template('youtube.html')

        try:
            from speech.transcriber import transcribe_youtube
            transcript, error = transcribe_youtube(yt_url, app.config['UPLOAD_FOLDER'], language=language)

            if error:
                flash(error, 'error')
                return render_template('youtube.html')

            if not transcript or len(transcript.strip()) < 20:
                flash('Could not extract text from this video. Try a video with captions.', 'error')
                return render_template('youtube.html')

            p = run_pipeline(transcript, tone)
            result_id = save_result(
                input_type='youtube', input_text=transcript,
                summary=p['summary'], highlights=p['highlights'],
                script=p['script'], social_posts=p['social_posts'],
                keywords=p['keywords'], tone=tone,
                hashtags=p['hashtags'], titles=p['titles'],
                twitter_thread=p['twitter_thread'], linkedin_post=p['linkedin_post']
            )
            return redirect(url_for('result', result_id=result_id))

        except Exception as e:
            flash(f'Processing error: {str(e)}', 'error')
            return render_template('youtube.html')

    return render_template('youtube.html')


@app.route('/tools', methods=['GET', 'POST'])
def tools():
    """Quick tools page — run individual tools without saving."""
    result = None
    active_tool = request.args.get('tool', request.form.get('tool', 'summarize'))

    if request.method == 'POST':
        tool  = request.form.get('tool', 'summarize')
        text  = request.form.get('text', '').strip()
        tone  = request.form.get('tone', 'professional')

        if not text or len(text) < 30:
            flash('Please enter at least 30 characters of text.', 'error')
            return render_template('tools.html', result=None, active_tool=tool)

        result = {'tool': tool, 'text': text}

        if tool == 'summarize':
            result['output'] = chunk_and_summarize(text)
        elif tool == 'keywords':
            kws = extract_keywords(text, top_n=15)
            result['output'] = kws
            result['hashtags'] = generate_hashtags(text, kws)
        elif tool == 'hashtags':
            kws = extract_keywords(text, top_n=15)
            result['output'] = hashtags_by_platform(text, kws)
        elif tool == 'titles':
            result['output'] = generate_titles(text, count=10)
        elif tool == 'thread':
            thread = split_into_thread(text, tone)
            result['output'] = thread
            result['thread_preview'] = format_thread_preview(thread)
        elif tool == 'linkedin':
            kws = extract_keywords(text)
            highlights = extract_highlights(text)
            summary = chunk_and_summarize(text)
            result['output'] = convert_blog_to_linkedin(text, summary, highlights, kws, tone)

        return render_template('tools.html', result=result, active_tool=tool)

    return render_template('tools.html', result=None, active_tool=active_tool)


@app.route('/result/<int:result_id>')
def result(result_id):
    data = get_result_by_id(result_id)
    if not data:
        flash('Result not found.', 'error')
        return redirect(url_for('index'))
    return render_template('result.html', data=data)


@app.route('/history')
def history():
    results = get_all_results()
    return render_template('history.html', results=results)


@app.route('/api/process_blog', methods=['POST'])
def api_process_blog():
    payload = request.get_json()
    if not payload:
        return jsonify({'error': 'No JSON body'}), 400
    text = payload.get('text', '')
    tone = payload.get('tone', 'professional')
    if len(text) < 50:
        return jsonify({'error': 'Text too short'}), 400
    p = run_pipeline(text, tone)
    return jsonify(p)


# ─────────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    print("\n🚀  AI Content Repurposer running at http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)
