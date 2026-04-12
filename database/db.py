import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'content.db')


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_type TEXT NOT NULL,
            input_preview TEXT,
            full_transcript TEXT,
            summary TEXT,
            highlights TEXT,
            script TEXT,
            social_posts TEXT,
            keywords TEXT,
            tone TEXT,
            hashtags TEXT,
            titles TEXT,
            twitter_thread TEXT,
            linkedin_post TEXT,
            created_at TEXT
        )
    ''')
    # Migrate existing DB — add new columns if missing
    existing = [row[1] for row in c.execute("PRAGMA table_info(results)").fetchall()]
    for col in ['hashtags', 'titles', 'twitter_thread', 'linkedin_post', 'full_transcript']:
        if col not in existing:
            c.execute(f"ALTER TABLE results ADD COLUMN {col} TEXT")
    conn.commit()
    conn.close()


def save_result(input_type, input_text, summary, highlights, script, social_posts, keywords, tone,
                hashtags=None, titles=None, twitter_thread=None, linkedin_post=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO results (input_type, input_preview, full_transcript, summary, highlights, script,
                             social_posts, keywords, tone, hashtags, titles, twitter_thread,
                             linkedin_post, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        input_type,
        input_text[:300],
        input_text,           # full text — no truncation
        summary,
        json.dumps(highlights),
        script,
        json.dumps(social_posts),
        json.dumps(keywords),
        tone,
        json.dumps(hashtags) if hashtags else None,
        json.dumps(titles) if titles else None,
        json.dumps(twitter_thread) if twitter_thread else None,
        linkedin_post,
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))
    result_id = c.lastrowid
    conn.commit()
    conn.close()
    return result_id


def get_result_by_id(result_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM results WHERE id = ?', (result_id,))
    row = c.fetchone()
    conn.close()
    if row:
        data = dict(row)
        data['highlights']     = json.loads(data['highlights'])
        data['social_posts']   = json.loads(data['social_posts'])
        data['keywords']       = json.loads(data['keywords'])
        data['hashtags']       = json.loads(data['hashtags']) if data.get('hashtags') else []
        data['titles']         = json.loads(data['titles']) if data.get('titles') else []
        data['twitter_thread'] = json.loads(data['twitter_thread']) if data.get('twitter_thread') else []
        return data
    return None


def get_all_results():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT id, input_type, input_preview, tone, created_at FROM results ORDER BY id DESC LIMIT 20')
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]
