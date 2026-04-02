import { useState } from "react";

const TABS = [
  { key: "blog_article",       label: "Blog",      icon: "📝" },
  { key: "linkedin_post",      label: "LinkedIn",  icon: "💼" },
  { key: "twitter_thread",     label: "Twitter",   icon: "🐦" },
  { key: "instagram_captions", label: "Instagram", icon: "📸" },
  { key: "video_script",       label: "Video",     icon: "🎬" },
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
    <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
      <div className="tab-group">
        {TABS.map((t) => (
          <button key={t.key} className={`tab-item ${active === t.key ? "active" : ""}`}
            onClick={() => setActive(t.key)}>
            <span>{t.icon}</span> {t.label}
          </button>
        ))}
      </div>
      <div className="output-content fade-in" key={active}>
        <div className="output-toolbar">
          <span className="output-title">
            {TABS.find((t) => t.key === active)?.icon} {TABS.find((t) => t.key === active)?.label}
          </span>
          <button className={`btn-copy ${copied ? "done" : ""}`} onClick={handleCopy}>
            {copied ? "✓ Copied" : "Copy"}
          </button>
        </div>
        <pre className="output-pre">{data[active]}</pre>
      </div>
    </div>
  );
}
