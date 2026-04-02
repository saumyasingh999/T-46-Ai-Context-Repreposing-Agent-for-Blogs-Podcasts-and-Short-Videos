import { useState } from "react";

export default function LinkedInPreview({ data }) {
  const [copied, setCopied] = useState(false);
  const [expanded, setExpanded] = useState(false);

  function handleCopy() {
    navigator.clipboard.writeText(data.full_post);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  const lines = data.full_post.split("\n");
  const hasMore = lines.length > 3;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: ".9rem" }}>
      <div className="stats-bar">
        {[
          { icon: "📝", val: data.word_count, label: "words" },
          { icon: "⏱", val: data.estimated_read_time },
          { icon: "#", val: data.hashtags.length, label: "hashtags" },
        ].map((item, i) => (
          <div key={i} style={{ display: "flex", alignItems: "center", gap: ".35rem" }}>
            {i > 0 && <div className="stat-div" />}
            <span style={{ fontSize: ".82rem" }}>{item.icon}</span>
            <span className="stat-val">{item.val}</span>
            {item.label && <span className="stat-lbl">{item.label}</span>}
          </div>
        ))}
      </div>

      <div className="anatomy">
        {[{ label: "🪝 Hook", text: data.hook }, { label: "📄 Body", text: data.body }, { label: "🎯 CTA", text: data.cta }]
          .map((sec, i) => (
            <div key={i}>
              {i > 0 && <div className="anatomy-div" />}
              <div className="anatomy-sec">
                <span className="anatomy-lbl">{sec.label}</span>
                <div className="anatomy-txt">{sec.text}</div>
              </div>
            </div>
          ))}
        <div className="anatomy-div" />
        <div className="anatomy-sec">
          <span className="anatomy-lbl">🏷 Hashtags</span>
          <div style={{ display: "flex", gap: ".4rem", flexWrap: "wrap", marginTop: ".25rem" }}>
            {data.hashtags.map((tag) => (
              <span key={tag} className="tag tag-teal">#{tag.replace(/^#/, "")}</span>
            ))}
          </div>
        </div>
      </div>

      <div className="li-card">
        <div className="li-head">
          <div className="li-avatar">AI</div>
          <div>
            <div className="li-name">Your Name</div>
            <div className="li-meta">Content Creator • Just now</div>
          </div>
          <div className="li-logo">in</div>
        </div>
        <div className="li-body">
          <p className="li-post-text">
            {expanded || !hasMore ? data.full_post : lines.slice(0, 3).join("\n")}
          </p>
          {hasMore && (
            <button className="li-see-more" onClick={() => setExpanded(!expanded)}>
              {expanded ? "see less" : "...see more"}
            </button>
          )}
        </div>
        <div className="li-foot">
          {["👍 Like", "💬 Comment", "🔁 Repost", "📤 Send"].map((r) => (
            <span key={r} className="li-reaction">{r}</span>
          ))}
        </div>
      </div>

      <button className="btn btn-primary"
        style={copied ? { background: "linear-gradient(135deg,#059669,#047857)" } : {}}
        onClick={handleCopy}>
        {copied ? "✓ Copied to clipboard!" : "Copy Post"}
      </button>
    </div>
  );
}
