import { useState } from "react";

const inputTypes = [
  { id: "youtube", label: "YouTube URL" },
  { id: "blog", label: "Blog Text" },
  { id: "audio", label: "Audio File" },
];

export default function InputForm({ onSubmit, loading }) {
  const [activeType, setActiveType] = useState("youtube");
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [blogText, setBlogText] = useState("");
  const [audioFile, setAudioFile] = useState(null);

  function handleSubmit(e) {
    e.preventDefault();
    onSubmit({ youtubeUrl, blogText, audioFile, activeType });
  }

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <div style={styles.tabs}>
        {inputTypes.map((t) => (
          <button
            key={t.id}
            type="button"
            onClick={() => setActiveType(t.id)}
            style={{ ...styles.tab, ...(activeType === t.id ? styles.tabActive : {}) }}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div style={styles.inputArea}>
        {activeType === "youtube" && (
          <input
            style={styles.input}
            type="url"
            placeholder="https://www.youtube.com/watch?v=..."
            value={youtubeUrl}
            onChange={(e) => setYoutubeUrl(e.target.value)}
            required
          />
        )}
        {activeType === "blog" && (
          <textarea
            style={{ ...styles.input, ...styles.textarea }}
            placeholder="Paste your blog text here..."
            value={blogText}
            onChange={(e) => setBlogText(e.target.value)}
            required
          />
        )}
        {activeType === "audio" && (
          <div style={styles.fileWrap}>
            <label style={styles.fileLabel}>
              <span>{audioFile ? audioFile.name : "Click to upload audio file (mp3, wav, m4a)"}</span>
              <input
                type="file"
                accept="audio/*"
                style={{ display: "none" }}
                onChange={(e) => setAudioFile(e.target.files[0])}
                required
              />
            </label>
          </div>
        )}
      </div>

      <button type="submit" disabled={loading} style={{ ...styles.btn, ...(loading ? styles.btnDisabled : {}) }}>
        {loading ? "Processing..." : "Generate Content"}
      </button>
    </form>
  );
}

const styles = {
  form: { display: "flex", flexDirection: "column", gap: "1.25rem" },
  tabs: { display: "flex", gap: "0.5rem" },
  tab: {
    padding: "0.5rem 1.25rem",
    borderRadius: "8px",
    border: "1px solid #2d2d44",
    background: "transparent",
    color: "#94a3b8",
    cursor: "pointer",
    fontSize: "0.875rem",
    transition: "all 0.2s",
  },
  tabActive: {
    background: "#4f46e5",
    borderColor: "#4f46e5",
    color: "#fff",
  },
  inputArea: {},
  input: {
    width: "100%",
    padding: "0.875rem 1rem",
    borderRadius: "10px",
    border: "1px solid #2d2d44",
    background: "#1a1a2e",
    color: "#e2e8f0",
    fontSize: "0.95rem",
    outline: "none",
    transition: "border-color 0.2s",
  },
  textarea: { minHeight: "160px", resize: "vertical" },
  fileWrap: { width: "100%" },
  fileLabel: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "2rem",
    borderRadius: "10px",
    border: "2px dashed #2d2d44",
    color: "#64748b",
    cursor: "pointer",
    fontSize: "0.9rem",
    transition: "border-color 0.2s",
  },
  btn: {
    padding: "0.875rem",
    borderRadius: "10px",
    border: "none",
    background: "linear-gradient(135deg, #4f46e5, #7c3aed)",
    color: "#fff",
    fontSize: "1rem",
    fontWeight: "600",
    cursor: "pointer",
    transition: "opacity 0.2s",
  },
  btnDisabled: { opacity: 0.6, cursor: "not-allowed" },
};
