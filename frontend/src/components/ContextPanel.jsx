export default function ContextPanel({ data }) {
  return (
    <div style={styles.container}>
      <div style={styles.grid}>

        <div style={styles.card}>
          <div style={styles.label}>Main Topic</div>
          <div style={styles.value}>{data.main_topic}</div>
        </div>

        <div style={styles.card}>
          <div style={styles.label}>Target Audience</div>
          <div style={styles.value}>{data.target_audience}</div>
        </div>

        <div style={{ ...styles.card, ...styles.fullWidth }}>
          <div style={styles.label}>Tone</div>
          <div style={styles.toneWrap}>
            {data.tone.split(",").map((t) => (
              <span key={t} style={styles.badge}>{t.trim()}</span>
            ))}
          </div>
        </div>

        <div style={{ ...styles.card, ...styles.fullWidth }}>
          <div style={styles.label}>Key Insights</div>
          <ul style={styles.list}>
            {data.key_insights.map((insight, i) => (
              <li key={i} style={styles.listItem}>
                <span style={styles.bullet}>→</span> {insight}
              </li>
            ))}
          </ul>
        </div>

        {data.important_quotes.length > 0 && (
          <div style={{ ...styles.card, ...styles.fullWidth }}>
            <div style={styles.label}>Important Quotes</div>
            {data.important_quotes.map((q, i) => (
              <blockquote key={i} style={styles.quote}>"{q}"</blockquote>
            ))}
          </div>
        )}

        <div style={{ ...styles.card, ...styles.fullWidth }}>
          <div style={styles.label}>Content Structure</div>
          <div style={styles.structureGrid}>
            {["intro", "body", "conclusion"].map((section) => (
              <div key={section} style={styles.structureItem}>
                <div style={styles.structureLabel}>{section.charAt(0).toUpperCase() + section.slice(1)}</div>
                <div style={styles.structureText}>{data.content_structure[section]}</div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}

const styles = {
  container: { width: "100%" },
  grid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.75rem" },
  card: {
    background: "#1a1a2e",
    border: "1px solid #2d2d44",
    borderRadius: "10px",
    padding: "1rem",
  },
  fullWidth: { gridColumn: "1 / -1" },
  label: {
    fontSize: "0.7rem",
    fontWeight: "600",
    textTransform: "uppercase",
    letterSpacing: "0.08em",
    color: "#6366f1",
    marginBottom: "0.5rem",
  },
  value: { fontSize: "0.95rem", color: "#e2e8f0", lineHeight: "1.5" },
  toneWrap: { display: "flex", gap: "0.5rem", flexWrap: "wrap" },
  badge: {
    padding: "0.25rem 0.75rem",
    borderRadius: "999px",
    background: "rgba(99,102,241,0.15)",
    border: "1px solid rgba(99,102,241,0.3)",
    color: "#a5b4fc",
    fontSize: "0.8rem",
  },
  list: { listStyle: "none", display: "flex", flexDirection: "column", gap: "0.5rem" },
  listItem: { display: "flex", gap: "0.5rem", fontSize: "0.9rem", color: "#cbd5e1", lineHeight: "1.5" },
  bullet: { color: "#6366f1", flexShrink: 0, marginTop: "1px" },
  quote: {
    borderLeft: "3px solid #6366f1",
    paddingLeft: "1rem",
    margin: "0.5rem 0",
    color: "#94a3b8",
    fontStyle: "italic",
    fontSize: "0.9rem",
    lineHeight: "1.6",
  },
  structureGrid: { display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "0.75rem", marginTop: "0.25rem" },
  structureItem: {
    background: "#13131f",
    borderRadius: "8px",
    padding: "0.75rem",
    border: "1px solid #2d2d44",
  },
  structureLabel: {
    fontSize: "0.75rem",
    fontWeight: "600",
    color: "#7c3aed",
    marginBottom: "0.4rem",
    textTransform: "uppercase",
  },
  structureText: { fontSize: "0.85rem", color: "#94a3b8", lineHeight: "1.5" },
};
