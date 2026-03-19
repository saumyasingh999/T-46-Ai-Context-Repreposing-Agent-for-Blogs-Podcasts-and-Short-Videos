import { useState } from "react";

export default function LinkedInPreview({ data }) {
  const [copied, setCopied] = useState(false);
  const [expanded, setExpanded] = useState(false);

  function handleCopy() {
    navigator.clipboard.writeText(data.full_post);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  // Simulate LinkedIn "see more" fold at ~3 lines
  const lines = data.full_post.split("\n");
  const preview = lines.slice(0, 3).join("\n");
  const hasMore = lines.length > 3;

  return (
    <div style={styles.wrapper}>
      {/* Stats bar */}
      <div style={styles.statsBar}>
        <div style={styles.stat}>
          <span style={styles.statIcon}>📝</span>
          <span style={styles.statVal}>{data.word_count}</span>
          <span style={styles.statLabel}>words</span>
        </div>
        <div style={styles.statDivider} />
        <div style={styles.stat}>
          <span style={styles.statIcon}>⏱</span>
          <span style={styles.statVal}>{data.estimated_read_time}</span>
        </div>
        <div style={styles.statDivider} />
        <div style={styles.stat}>
          <span style={styles.statIcon}>#</span>
          <span style={styles.statVal}>{data.hashtags.length}</span>
          <span style={styles.statLabel}>hashtags</span>
        </div>
      </div>

      {/* Anatomy breakdown */}
      <div style={styles.anatomy}>
        <div style={styles.anatomySection}>
          <span style={styles.anatomyLabel}>🪝 Hook</span>
          <p style={styles.anatomyText}>{data.hook}</p>
        </div>
        <div style={styles.anatomyDivider} />
        <div style={styles.anatomySection}>
          <span style={styles.anatomyLabel}>📄 Body</span>
          <p style={styles.anatomyText}>{data.body}</p>
        </div>
        <div style={styles.anatomyDivider} />
        <div style={styles.anatomySection}>
          <span style={styles.anatomyLabel}>🎯 CTA</span>
          <p style={styles.anatomyText}>{data.cta}</p>
        </div>
        <div style={styles.anatomyDivider} />
        <div style={styles.anatomySection}>
          <span style={styles.anatomyLabel}>🏷 Hashtags</span>
          <div style={styles.hashtagRow}>
            {data.hashtags.map((tag) => (
              <span key={tag} style={styles.hashtag}>
                #{tag.replace(/^#/, "")}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* LinkedIn card mockup */}
      <div style={styles.card}>
        <div style={styles.cardHeader}>
          <div style={styles.avatar}>AI</div>
          <div>
            <div style={styles.authorName}>Your Name</div>
            <div style={styles.authorMeta}>Content Creator • 1st • Just now</div>
          </div>
          <div style={styles.liLogo}>in</div>
        </div>

        <div style={styles.postBody}>
          <p style={styles.postText}>
            {expanded || !hasMore ? data.full_post : preview}
          </p>
          {hasMore && (
            <button onClick={() => setExpanded(!expanded)} style={styles.seeMore}>
              {expanded ? "see less" : "...see more"}
            </button>
          )}
        </div>

        <div style={styles.cardFooter}>
          <span style={styles.reaction}>👍 Like</span>
          <span style={styles.reaction}>💬 Comment</span>
          <span style={styles.reaction}>🔁 Repost</span>
          <span style={styles.reaction}>📤 Send</span>
        </div>
      </div>

      {/* Copy button */}
      <button onClick={handleCopy} style={styles.copyBtn}>
        {copied ? "✓ Copied to clipboard!" : "Copy Post"}
      </button>
    </div>
  );
}

const styles = {
  wrapper: { display: "flex", flexDirection: "column", gap: "1rem" },

  statsBar: {
    display: "flex",
    gap: "1rem",
    alignItems: "center",
    background: "#0e0e1a",
    border: "1px solid #2d2d44",
    borderRadius: "10px",
    padding: "0.75rem 1.25rem",
  },
  stat: { display: "flex", alignItems: "center", gap: "0.35rem" },
  statIcon: { fontSize: "0.85rem" },
  statVal: { fontSize: "0.9rem", fontWeight: "600", color: "#e2e8f0" },
  statLabel: { fontSize: "0.75rem", color: "#64748b" },
  statDivider: { width: "1px", height: "16px", background: "#2d2d44", margin: "0 0.25rem" },

  anatomy: {
    background: "#0e0e1a",
    border: "1px solid #2d2d44",
    borderRadius: "10px",
    overflow: "hidden",
  },
  anatomySection: { padding: "0.85rem 1.25rem" },
  anatomyDivider: { height: "1px", background: "#2d2d44" },
  anatomyLabel: {
    display: "block",
    fontSize: "0.7rem",
    fontWeight: "700",
    textTransform: "uppercase",
    letterSpacing: "0.08em",
    color: "#6366f1",
    marginBottom: "0.4rem",
  },
  anatomyText: {
    fontSize: "0.875rem",
    color: "#cbd5e1",
    lineHeight: "1.6",
    margin: 0,
    whiteSpace: "pre-wrap",
  },
  hashtagRow: { display: "flex", gap: "0.5rem", flexWrap: "wrap" },
  hashtag: {
    padding: "0.2rem 0.65rem",
    borderRadius: "999px",
    background: "rgba(99,102,241,0.12)",
    border: "1px solid rgba(99,102,241,0.25)",
    color: "#a5b4fc",
    fontSize: "0.8rem",
  },

  // LinkedIn card mockup
  card: {
    background: "#1e1e2e",
    border: "1px solid #2d2d44",
    borderRadius: "12px",
    overflow: "hidden",
  },
  cardHeader: {
    display: "flex",
    alignItems: "center",
    gap: "0.75rem",
    padding: "1rem 1.25rem 0.75rem",
    borderBottom: "1px solid #2d2d44",
  },
  avatar: {
    width: "42px",
    height: "42px",
    borderRadius: "50%",
    background: "linear-gradient(135deg, #4f46e5, #7c3aed)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "0.75rem",
    fontWeight: "700",
    color: "#fff",
    flexShrink: 0,
  },
  authorName: { fontSize: "0.9rem", fontWeight: "600", color: "#e2e8f0" },
  authorMeta: { fontSize: "0.75rem", color: "#64748b", marginTop: "1px" },
  liLogo: {
    marginLeft: "auto",
    width: "28px",
    height: "28px",
    background: "#0a66c2",
    borderRadius: "4px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    color: "#fff",
    fontWeight: "700",
    fontSize: "0.85rem",
  },
  postBody: { padding: "1rem 1.25rem" },
  postText: {
    fontSize: "0.9rem",
    color: "#cbd5e1",
    lineHeight: "1.7",
    whiteSpace: "pre-wrap",
    margin: 0,
  },
  seeMore: {
    background: "none",
    border: "none",
    color: "#6366f1",
    cursor: "pointer",
    fontSize: "0.875rem",
    padding: "0.25rem 0 0",
    display: "block",
  },
  cardFooter: {
    display: "flex",
    gap: "0",
    borderTop: "1px solid #2d2d44",
    padding: "0.5rem 0.5rem",
  },
  reaction: {
    flex: 1,
    textAlign: "center",
    fontSize: "0.8rem",
    color: "#64748b",
    padding: "0.4rem",
    borderRadius: "6px",
    cursor: "default",
  },

  copyBtn: {
    padding: "0.75rem",
    borderRadius: "10px",
    border: "none",
    background: "linear-gradient(135deg, #0a66c2, #0077b5)",
    color: "#fff",
    fontSize: "0.9rem",
    fontWeight: "600",
    cursor: "pointer",
    transition: "opacity 0.2s",
  },
};
