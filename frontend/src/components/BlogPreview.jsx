import ReactMarkdown from "react-markdown";
import { useState } from "react";

export default function BlogPreview({ data }) {
  const [copied, setCopied] = useState(false);
  const [view, setView] = useState("preview"); // "preview" | "markdown"

  function handleCopy() {
    const full = `# ${data.seo_title}\n\n> ${data.meta_description}\n\n${data.blog_markdown}`;
    navigator.clipboard.writeText(full);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div style={styles.container}>
      {/* SEO Meta bar */}
      <div style={styles.metaBar}>
        <div style={styles.metaItem}>
          <span style={styles.metaLabel}>SEO Title</span>
          <span style={styles.metaValue}>{data.seo_title}</span>
          <span style={styles.charCount}>{data.seo_title.length} chars</span>
        </div>
        <div style={styles.metaDivider} />
        <div style={styles.metaItem}>
          <span style={styles.metaLabel}>Meta Description</span>
          <span style={styles.metaValue}>{data.meta_description}</span>
          <span style={styles.charCount}>{data.meta_description.length} chars</span>
        </div>
      </div>

      {/* Toolbar */}
      <div style={styles.toolbar}>
        <div style={styles.viewToggle}>
          <button
            onClick={() => setView("preview")}
            style={{ ...styles.toggleBtn, ...(view === "preview" ? styles.toggleActive : {}) }}
          >
            Preview
          </button>
          <button
            onClick={() => setView("markdown")}
            style={{ ...styles.toggleBtn, ...(view === "markdown" ? styles.toggleActive : {}) }}
          >
            Markdown
          </button>
        </div>
        <button onClick={handleCopy} style={styles.copyBtn}>
          {copied ? "Copied!" : "Copy All"}
        </button>
      </div>

      {/* Content */}
      <div style={styles.content}>
        {view === "preview" ? (
          <div style={styles.prose}>
            <ReactMarkdown
              components={{
                h1: ({ children }) => <h1 style={styles.h1}>{children}</h1>,
                h2: ({ children }) => <h2 style={styles.h2}>{children}</h2>,
                h3: ({ children }) => <h3 style={styles.h3}>{children}</h3>,
                p: ({ children }) => <p style={styles.p}>{children}</p>,
                ul: ({ children }) => <ul style={styles.ul}>{children}</ul>,
                ol: ({ children }) => <ol style={styles.ol}>{children}</ol>,
                li: ({ children }) => <li style={styles.li}>{children}</li>,
                strong: ({ children }) => <strong style={styles.strong}>{children}</strong>,
                blockquote: ({ children }) => <blockquote style={styles.blockquote}>{children}</blockquote>,
                hr: () => <hr style={styles.hr} />,
              }}
            >
              {data.blog_markdown}
            </ReactMarkdown>
          </div>
        ) : (
          <pre style={styles.raw}>{`# ${data.seo_title}\n\n> ${data.meta_description}\n\n${data.blog_markdown}`}</pre>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: { display: "flex", flexDirection: "column", gap: "0" },
  metaBar: {
    background: "#0e0e1a",
    border: "1px solid #2d2d44",
    borderRadius: "10px",
    padding: "1rem",
    marginBottom: "0.75rem",
    display: "flex",
    flexDirection: "column",
    gap: "0.75rem",
  },
  metaItem: { display: "flex", alignItems: "baseline", gap: "0.75rem", flexWrap: "wrap" },
  metaLabel: {
    fontSize: "0.7rem",
    fontWeight: "700",
    textTransform: "uppercase",
    letterSpacing: "0.08em",
    color: "#6366f1",
    flexShrink: 0,
    minWidth: "110px",
  },
  metaValue: { fontSize: "0.875rem", color: "#e2e8f0", flex: 1 },
  charCount: {
    fontSize: "0.7rem",
    color: "#475569",
    background: "#1a1a2e",
    padding: "0.15rem 0.5rem",
    borderRadius: "999px",
    flexShrink: 0,
  },
  metaDivider: { height: "1px", background: "#2d2d44" },
  toolbar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "0.75rem 1rem",
    background: "#16162a",
    borderRadius: "10px 10px 0 0",
    border: "1px solid #2d2d44",
    borderBottom: "none",
  },
  viewToggle: {
    display: "flex",
    background: "#0e0e1a",
    borderRadius: "6px",
    padding: "2px",
    gap: "2px",
  },
  toggleBtn: {
    padding: "0.3rem 0.85rem",
    borderRadius: "5px",
    border: "none",
    background: "transparent",
    color: "#64748b",
    cursor: "pointer",
    fontSize: "0.8rem",
    transition: "all 0.15s",
  },
  toggleActive: { background: "#4f46e5", color: "#fff" },
  copyBtn: {
    padding: "0.35rem 0.85rem",
    borderRadius: "6px",
    border: "1px solid #4f46e5",
    background: "transparent",
    color: "#a5b4fc",
    cursor: "pointer",
    fontSize: "0.8rem",
  },
  content: {
    background: "#1a1a2e",
    border: "1px solid #2d2d44",
    borderRadius: "0 0 10px 10px",
    maxHeight: "600px",
    overflowY: "auto",
  },
  prose: { padding: "2rem 2.5rem" },
  raw: {
    padding: "1.5rem",
    whiteSpace: "pre-wrap",
    wordBreak: "break-word",
    fontSize: "0.85rem",
    color: "#94a3b8",
    lineHeight: "1.7",
    margin: 0,
  },
  h1: { fontSize: "1.75rem", fontWeight: "700", color: "#e2e8f0", marginBottom: "1rem", lineHeight: "1.3" },
  h2: {
    fontSize: "1.3rem", fontWeight: "600", color: "#a5b4fc",
    marginTop: "2rem", marginBottom: "0.75rem",
    paddingBottom: "0.4rem", borderBottom: "1px solid #2d2d44",
  },
  h3: { fontSize: "1.1rem", fontWeight: "600", color: "#c4b5fd", marginTop: "1.5rem", marginBottom: "0.5rem" },
  p: { color: "#cbd5e1", lineHeight: "1.8", marginBottom: "1rem", fontSize: "0.95rem" },
  ul: { paddingLeft: "1.5rem", marginBottom: "1rem" },
  ol: { paddingLeft: "1.5rem", marginBottom: "1rem" },
  li: { color: "#cbd5e1", lineHeight: "1.8", marginBottom: "0.35rem", fontSize: "0.95rem" },
  strong: { color: "#e2e8f0", fontWeight: "600" },
  blockquote: {
    borderLeft: "3px solid #6366f1",
    paddingLeft: "1rem",
    margin: "1rem 0",
    color: "#94a3b8",
    fontStyle: "italic",
  },
  hr: { border: "none", borderTop: "1px solid #2d2d44", margin: "1.5rem 0" },
};
