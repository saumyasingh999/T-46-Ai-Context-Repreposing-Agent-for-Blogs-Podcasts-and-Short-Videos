import { useState } from "react";

const TYPE_CFG = {
  hook: { label: "Hook", color: "#d97706", bg: "rgba(217,119,6,.07)",  border: "rgba(217,119,6,.2)"  },
  body: { label: "Body", color: "#5b4fcf", bg: "rgba(91,79,207,.06)",  border: "rgba(91,79,207,.18)" },
  cta:  { label: "CTA",  color: "#0ea5e9", bg: "rgba(14,165,233,.06)", border: "rgba(14,165,233,.2)" },
};

function CharBar({ count }) {
  const pct = Math.min((count / 280) * 100, 100);
  const color = count > 280 ? "var(--red)" : count > 240 ? "var(--yellow)" : "var(--green)";
  return (
    <div className="char-bar-wrap">
      <div className="char-bar-track">
        <div className="char-bar-fill" style={{ width: `${pct}%`, background: color }} />
      </div>
      <span className="char-bar-label" style={{ color }}>{count}/280</span>
    </div>
  );
}

export default function TwitterThread({ data }) {
  const [copiedIdx, setCopiedIdx] = useState(null);
  const [copiedAll, setCopiedAll] = useState(false);

  function copyTweet(text, idx) {
    navigator.clipboard.writeText(text);
    setCopiedIdx(idx);
    setTimeout(() => setCopiedIdx(null), 2000);
  }
  function copyAll() {
    navigator.clipboard.writeText(data.tweets.map((t) => t.text).join("\n\n"));
    setCopiedAll(true);
    setTimeout(() => setCopiedAll(false), 2000);
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
      <div className="stats-bar">
        <div className="stat"><span>🐦</span><span className="stat-val">{data.total_tweets}</span><span className="stat-lbl">tweets</span></div>
        <div className="stat-div" />
        <div className="stat"><span>📈</span><span className="stat-val">{data.estimated_impressions}</span><span className="stat-lbl">est. impressions</span></div>
        <div className="stat-div" />
        <div className="stat" style={{ flex: 1 }}>
          <span style={{ fontSize: ".78rem", color: "var(--text2)" }}>{data.thread_summary}</span>
        </div>
        <button className={`btn btn-primary btn-sm ${copiedAll ? "done" : ""}`}
          style={{ borderRadius: "999px", ...(copiedAll ? { background: "linear-gradient(135deg,#059669,#047857)" } : {}) }}
          onClick={copyAll}>
          {copiedAll ? "✓ Copied!" : "Copy Thread"}
        </button>
      </div>

      <div style={{ display: "flex", flexDirection: "column" }}>
        {data.tweets.map((tweet, idx) => {
          const cfg = TYPE_CFG[tweet.type] || TYPE_CFG.body;
          const isLast = idx === data.tweets.length - 1;
          return (
            <div key={tweet.number} className="tweet-row fade-up">
              <div className="tweet-connector">
                <div className="tweet-num" style={{ background: cfg.color }}>{tweet.number}</div>
                {!isLast && <div className="tweet-line" />}
              </div>
              <div className="tweet-card" style={{ borderColor: cfg.border, background: cfg.bg }}>
                <div className="tweet-top">
                  <span className="tweet-badge" style={{ color: cfg.color, borderColor: cfg.border }}>{cfg.label}</span>
                  <button className={`btn-copy ${copiedIdx === idx ? "done" : ""}`}
                    onClick={() => copyTweet(tweet.text, idx)}>
                    {copiedIdx === idx ? "✓" : "Copy"}
                  </button>
                </div>
                <p className="tweet-text">{tweet.text}</p>
                <CharBar count={tweet.char_count} />
                {tweet.over_limit && (
                  <p style={{ marginTop: ".4rem", fontSize: ".72rem", color: "var(--red)" }}>
                    ⚠ Over 280 chars — trim before posting
                  </p>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
