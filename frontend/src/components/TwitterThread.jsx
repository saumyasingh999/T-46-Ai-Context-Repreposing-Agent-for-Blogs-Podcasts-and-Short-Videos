import { useState } from "react";

const TYPE_CONFIG = {
  hook:  { label: "Hook",  color: "#f59e0b", bg: "rgba(245,158,11,0.1)",  border: "rgba(245,158,11,0.25)" },
  body:  { label: "Body",  color: "#6366f1", bg: "rgba(99,102,241,0.08)", border: "rgba(99,102,241,0.2)"  },
  cta:   { label: "CTA",   color: "#10b981", bg: "rgba(16,185,129,0.1)",  border: "rgba(16,185,129,0.25)" },
};

function CharBar({ count }) {
  const pct = Math.min((count / 280) * 100, 100);
  const over = count > 280;
  const color = over ? "#f87171" : count > 240 ? "#f59e0b" : "#10b981";
  return (
    <div style={barStyles.wrap}>
      <div style={{ ...barStyles.track }}>
        <div style={{ ...barStyles.fill, width: `${pct}%`, background: color }} />
      </div>
      <span style={{ ...barStyles.label, color }}>{count}/280</span>
    </div>
  );
}

const barStyles = {
  wrap: { display: "flex", alignItems: "center", gap: "0.5rem", marginTop: "0.5rem" },
  track: { flex: 1, height: "3px", background: "#2d2d44", borderRadius: "999px", overflow: "hidden" },
  fill: { height: "100%", borderRadius: "999px", transition: "width 0.3s" },
  label: { fontSize: "0.7rem", fontWeight: "600", minWidth: "48px", textAlign: "right" },
};

export default function TwitterThread({ data }) {
  const [copiedIdx, setCopiedIdx] = useState(null);
  const [copiedAll, setCopiedAll] = useState(false);

  function copyTweet(text, idx) {
    navigator.clipboard.writeText(text);
    setCopiedIdx(idx);
    setTimeout(() => setCopiedIdx(null), 2000);
  }

  function copyAll() {
    const full = data.tweets.map((t) => t.text).join("\n\n");
    navigator.clipboard.writeText(full);
    setCopiedAll(true);
    setTimeout(() => setCopiedAll(false), 2000);
  }

  return (
    <div style={styles.wrapper}>
      {/* Thread stats */}
      <div style={styles.statsBar}>
        <div style={styles.stat}>
          <span style={styles.statIcon}>🐦</span>
          <span style={styles.statVal}>{data.total_tweets}</span>
          <span style={styles.statLabel}>tweets</span>
        </div>
        <div style={styles.statDivider} />
        <div style={styles.stat}>
          <span style={styles.statIcon}>📈</span>
          <span style={styles.statVal}>{data.estimated_impressions}</span>
          <span style={styles.statLabel}>est. impressions</span>
        </div>
        <div style={styles.statDivider} />
        <div style={{ ...styles.stat, flex: 1 }}>
          <span style={styles.statIcon}>💡</span>
          <span style={{ ...styles.statLabel, color: "#94a3b8" }}>{data.thread_summary}</span>
        </div>
        <button onClick={copyAll} style={styles.copyAllBtn}>
          {copiedAll ? "✓ Copied!" : "Copy Thread"}
        </button>
      </div>

      {/* Tweet cards */}
      <div style={styles.thread}>
        {data.tweets.map((tweet, idx) => {
          const cfg = TYPE_CONFIG[tweet.type] || TYPE_CONFIG.body;
          const isLast = idx === data.tweets.length - 1;
          return (
            <div key={tweet.number} style={styles.row}>
              {/* Connector line */}
              <div style={styles.connectorCol}>
                <div style={{ ...styles.avatar, background: cfg.color }}>
                  {tweet.number}
                </div>
                {!isLast && <div style={styles.line} />}
              </div>

              {/* Tweet card */}
              <div style={{ ...styles.card, borderColor: cfg.border, background: cfg.bg }}>
                <div style={styles.cardTop}>
                  <span style={{ ...styles.typeBadge, color: cfg.color, borderColor: cfg.border }}>
                    {cfg.label}
                  </span>
                  <button
                    onClick={() => copyTweet(tweet.text, idx)}
                    style={styles.copyBtn}
                  >
                    {copiedIdx === idx ? "✓" : "Copy"}
                  </button>
                </div>

                <p style={styles.tweetText}>{tweet.text}</p>

                <CharBar count={tweet.char_count} />

                {tweet.over_limit && (
                  <p style={styles.overLimit}>⚠ Over 280 characters — trim before posting</p>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

const styles = {
  wrapper: { display: "flex", flexDirection: "column", gap: "1rem" },

  statsBar: {
    display: "flex",
    alignItems: "center",
    gap: "0.75rem",
    flexWrap: "wrap",
    background: "#0e0e1a",
    border: "1px solid #2d2d44",
    borderRadius: "10px",
    padding: "0.75rem 1.25rem",
  },
  stat: { display: "flex", alignItems: "center", gap: "0.35rem" },
  statIcon: { fontSize: "0.85rem" },
  statVal: { fontSize: "0.9rem", fontWeight: "600", color: "#e2e8f0" },
  statLabel: { fontSize: "0.75rem", color: "#64748b" },
  statDivider: { width: "1px", height: "16px", background: "#2d2d44" },
  copyAllBtn: {
    marginLeft: "auto",
    padding: "0.4rem 1rem",
    borderRadius: "999px",
    border: "none",
    background: "linear-gradient(135deg, #1d9bf0, #1a8cd8)",
    color: "#fff",
    fontSize: "0.8rem",
    fontWeight: "600",
    cursor: "pointer",
  },

  thread: { display: "flex", flexDirection: "column" },
  row: { display: "flex", gap: "0.75rem", alignItems: "flex-start" },

  connectorCol: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    flexShrink: 0,
    width: "32px",
  },
  avatar: {
    width: "32px",
    height: "32px",
    borderRadius: "50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "0.75rem",
    fontWeight: "700",
    color: "#fff",
    flexShrink: 0,
    zIndex: 1,
  },
  line: {
    width: "2px",
    flex: 1,
    minHeight: "16px",
    background: "#2d2d44",
    margin: "4px 0",
  },

  card: {
    flex: 1,
    border: "1px solid",
    borderRadius: "12px",
    padding: "0.875rem 1rem",
    marginBottom: "0.5rem",
  },
  cardTop: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "0.5rem",
  },
  typeBadge: {
    fontSize: "0.65rem",
    fontWeight: "700",
    textTransform: "uppercase",
    letterSpacing: "0.08em",
    border: "1px solid",
    borderRadius: "999px",
    padding: "0.15rem 0.6rem",
  },
  copyBtn: {
    padding: "0.2rem 0.65rem",
    borderRadius: "6px",
    border: "1px solid #2d2d44",
    background: "transparent",
    color: "#64748b",
    cursor: "pointer",
    fontSize: "0.75rem",
  },
  tweetText: {
    fontSize: "0.9rem",
    color: "#e2e8f0",
    lineHeight: "1.65",
    whiteSpace: "pre-wrap",
    margin: 0,
  },
  overLimit: {
    marginTop: "0.4rem",
    fontSize: "0.75rem",
    color: "#f87171",
  },
};
