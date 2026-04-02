import ReactMarkdown from "react-markdown";
import { useState } from "react";

export default function BlogPreview({ data }) {
  const [copied, setCopied] = useState(false);
  const [view, setView] = useState("preview");

  function handleCopy() {
    navigator.clipboard.writeText(`# ${data.seo_title}\n\n> ${data.meta_description}\n\n${data.blog_markdown}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: ".75rem" }}>
      <div className="meta-bar">
        {[{ label: "SEO Title", value: data.seo_title }, { label: "Meta Description", value: data.meta_description }]
          .map((item, i) => (
            <div key={i}>
              {i > 0 && <div className="meta-div" />}
              <div className="meta-row">
                <span className="meta-lbl">{item.label}</span>
                <span className="meta-val">{item.value}</span>
                <span className="char-count">{item.value.length} chars</span>
              </div>
            </div>
          ))}
      </div>

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div className="tab-group" style={{ flex: "none" }}>
          {["preview", "markdown"].map((v) => (
            <button key={v} className={`tab-item ${view === v ? "active" : ""}`}
              style={{ padding: ".3rem .75rem", fontSize: ".78rem" }} onClick={() => setView(v)}>
              {v.charAt(0).toUpperCase() + v.slice(1)}
            </button>
          ))}
        </div>
        <button className={`btn-copy ${copied ? "done" : ""}`} onClick={handleCopy}>
          {copied ? "✓ Copied" : "Copy All"}
        </button>
      </div>

      <div className="prose-area fade-in" key={view}>
        {view === "preview" ? (
          <div className="prose">
            <ReactMarkdown components={{
              h1: ({ children }) => <h1>{children}</h1>,
              h2: ({ children }) => <h2>{children}</h2>,
              h3: ({ children }) => <h3>{children}</h3>,
              p:  ({ children }) => <p>{children}</p>,
              ul: ({ children }) => <ul>{children}</ul>,
              ol: ({ children }) => <ol>{children}</ol>,
              li: ({ children }) => <li>{children}</li>,
              strong: ({ children }) => <strong>{children}</strong>,
              blockquote: ({ children }) => <blockquote>{children}</blockquote>,
              hr: () => <hr />,
            }}>
              {data.blog_markdown}
            </ReactMarkdown>
          </div>
        ) : (
          <pre className="raw-area">{`# ${data.seo_title}\n\n> ${data.meta_description}\n\n${data.blog_markdown}`}</pre>
        )}
      </div>
    </div>
  );
}
