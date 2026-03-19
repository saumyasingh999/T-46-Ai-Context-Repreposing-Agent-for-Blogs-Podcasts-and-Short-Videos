import { useState } from "react";

const TABS = [
  { key: "blog_article", label: "Blog Article", icon: "📝" },
  { key: "linkedin_post", label: "LinkedIn", icon: "💼" },
  { key: "twitter_thread", label: "Twitter Thread", icon: "🐦" },
  { key: "instagram_captions", label: "Instagram", icon: "📸" },
  { key: "video_script", label: "Video Script", icon: "🎬" },
];

export default function OutputTabs({ data }) {
  const [active, setActive] = useState("blog_article");
  const [copied, setCopied] = useState(false);

  function handleCopy() {
    navigator.clipboard.writeText(data[active]);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div style={styles.container}>
      <div style={styles.tabBar}>
        {TABS.map((t) => (
          <button
            key={t.key}
            onClick={() => setActive(t.key)}
            style={{ ...styles.tab, ...(active === t.key ? styles.tabActive : {}) }}
          >
            <span>{t.icon}</span> {t.label}
          </button>
        ))}
      </div>

      <div style={styles.content}>
        <div style={styles.toolbar}>
          <span style={styles.tabTitle}>{TABS.find((t) => t.key === active)?.label}</span>
          <button onClick={handleCopy} style={styles.copyBtn}>
            {copied ? "Copied!" : "Copy"}
          </button>
        </div>
        <pre style={styles.pre}>{data[active]}</pre>
      </div>
    </div>
  );
}

const styles = {
  container: { display: "flex", flexDirection: "column", gap: "0" },
  tabBar: {
    display: "flex",
    gap: "0.25rem",
    flexWrap: "wrap",
    borderBottom: "1px solid #2d2d44",
    paddingBottom: "0.5rem",
    marginBottom: "1rem",
  },
  tab: {
    display: "flex",
    alignItems: "center",
    gap: "0.4rem",
    padding: "0.5rem 1rem",
    borderRadius: "8px",
    border: "1px solid transparent",
    background: "transparent",
    color: "#64748b",
    cursor: "pointer",
    fontSize: "0.85rem",
    transition: "all 0.2s",
  },
  tabActive: {
    background: "#1e1e35",
    borderColor: "#4f46e5",
    color: "#a5b4fc",
  },
  content: {
    background: "#1a1a2e",
    borderRadius: "12px",
    border: "1px solid #2d2d44",
    overflow: "hidden",
  },
  toolbar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "0.75rem 1rem",
    borderBottom: "1px solid #2d2d44",
    background: "#16162a",
  },
  tabTitle: { fontSize: "0.875rem", fontWeight: "600", color: "#a5b4fc" },
  copyBtn: {
    padding: "0.35rem 0.85rem",
    borderRadius: "6px",
    border: "1px solid #4f46e5",
    background: "transparent",
    color: "#a5b4fc",
    cursor: "pointer",
    fontSize: "0.8rem",
    transition: "background 0.2s",
  },
  pre: {
    padding: "1.25rem",
    whiteSpace: "pre-wrap",
    wordBreak: "break-word",
    fontSize: "0.9rem",
    lineHeight: "1.7",
    color: "#cbd5e1",
    maxHeight: "500px",
    overflowY: "auto",
  },
};
