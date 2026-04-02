import { useState } from "react";

const TABS = [
  { id: "youtube", label: "YouTube URL", icon: "▶" },
  { id: "blog",    label: "Blog Text",   icon: "✍" },
  { id: "audio",   label: "Audio File",  icon: "🎙" },
];

export default function InputForm({ onSubmit, loading }) {
  const [activeType, setActiveType] = useState("youtube");
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [blogText, setBlogText]     = useState("");
  const [audioFile, setAudioFile]   = useState(null);

  function handleSubmit(e) {
    e.preventDefault();
    onSubmit({ youtubeUrl, blogText, audioFile, activeType });
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "1.1rem" }}>
      <div className="tab-group">
        {TABS.map((t) => (
          <button key={t.id} type="button"
            className={`tab-item ${activeType === t.id ? "active" : ""}`}
            onClick={() => setActiveType(t.id)}>
            <span>{t.icon}</span> {t.label}
          </button>
        ))}
      </div>

      <div className="fade-in" key={activeType}>
        {activeType === "youtube" && (
          <input type="url" placeholder="https://www.youtube.com/watch?v=..."
            value={youtubeUrl} onChange={(e) => setYoutubeUrl(e.target.value)} required />
        )}
        {activeType === "blog" && (
          <textarea placeholder="Paste your blog text here..."
            value={blogText} onChange={(e) => setBlogText(e.target.value)} required />
        )}
        {activeType === "audio" && (
          <label className="file-drop">
            <span className="file-icon">🎙</span>
            <span className="file-text">
              {audioFile ? audioFile.name : "Click to upload audio (mp3, wav, m4a)"}
            </span>
            <input type="file" accept="audio/*" style={{ display: "none" }}
              onChange={(e) => setAudioFile(e.target.files[0])} required />
          </label>
        )}
      </div>

      <button type="submit" disabled={loading} className="btn btn-primary" style={{ width: "100%" }}>
        {loading
          ? <><span className="spinner" style={{ width: 15, height: 15 }} /> Processing...</>
          : "Generate Content →"}
      </button>
    </form>
  );
}
