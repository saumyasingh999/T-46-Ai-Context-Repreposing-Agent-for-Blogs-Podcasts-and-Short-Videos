export default function ContextPanel({ data }) {
  return (
    <div className="grid-2">
      <div className="ctx-cell fade-up">
        <div className="ctx-label">Main Topic</div>
        <div className="ctx-value">{data.main_topic}</div>
      </div>
      <div className="ctx-cell fade-up">
        <div className="ctx-label">Target Audience</div>
        <div className="ctx-value">{data.target_audience}</div>
      </div>
      <div className="ctx-cell full fade-up">
        <div className="ctx-label">Tone</div>
        <div style={{ display: "flex", gap: ".5rem", flexWrap: "wrap", marginTop: ".25rem" }}>
          {data.tone.split(",").map((t) => <span key={t} className="tag">{t.trim()}</span>)}
        </div>
      </div>
      <div className="ctx-cell full fade-up">
        <div className="ctx-label">Key Insights</div>
        <ul style={{ listStyle: "none", marginTop: ".25rem" }}>
          {data.key_insights.map((ins, i) => (
            <li key={i} style={{ display: "flex", gap: ".5rem", fontSize: ".875rem", color: "var(--text2)", lineHeight: 1.55, marginBottom: ".4rem" }}>
              <span style={{ color: "var(--accent)", flexShrink: 0 }}>→</span> {ins}
            </li>
          ))}
        </ul>
      </div>
      {data.important_quotes?.length > 0 && (
        <div className="ctx-cell full fade-up">
          <div className="ctx-label">Quotes</div>
          {data.important_quotes.map((q, i) => (
            <blockquote key={i} className="insight">"{q}"</blockquote>
          ))}
        </div>
      )}
      <div className="ctx-cell full fade-up">
        <div className="ctx-label">Content Structure</div>
        <div className="struct-grid">
          {["intro", "body", "conclusion"].map((sec) => (
            <div key={sec} className="struct-item">
              <div className="struct-lbl">{sec.charAt(0).toUpperCase() + sec.slice(1)}</div>
              <div className="struct-txt">{data.content_structure[sec]}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
