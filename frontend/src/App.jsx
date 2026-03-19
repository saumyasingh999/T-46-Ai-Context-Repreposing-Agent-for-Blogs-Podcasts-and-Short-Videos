import { useState, useEffect } from "react";
import InputForm from "./components/InputForm";
import OutputTabs from "./components/OutputTabs";
import ContextPanel from "./components/ContextPanel";
import BlogPreview from "./components/BlogPreview";
import LinkedInPreview from "./components/LinkedInPreview";
import TwitterThread from "./components/TwitterThread";
import { checkHealth, ingestContent, extractContext, generateBlog, generateLinkedIn, generateTwitterThread, generateContent } from "./api";

export default function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [backendStatus, setBackendStatus] = useState("checking"); // checking | ok | down | no-key
  const [output, setOutput] = useState(null);
  const [context, setContext] = useState(null);
  const [blog, setBlog] = useState(null);
  const [linkedIn, setLinkedIn] = useState(null);
  const [thread, setThread] = useState(null);
  const [step, setStep] = useState("");

  // Health check on mount
  useEffect(() => {
    checkHealth()
      .then((data) => setBackendStatus(data.gemini_key_set ? "ok" : "no-key"))
      .catch(() => setBackendStatus("down"));
  }, []);

  async function handleSubmit({ youtubeUrl, blogText, audioFile }) {
    setLoading(true);
    setError(null);
    setOutput(null);
    setContext(null);
    setBlog(null);
    setLinkedIn(null);
    setThread(null);

    try {
      setStep("Extracting content...");
      const content = await ingestContent({ youtubeUrl, blogText, audioFile });

      setStep("Analyzing content...");
      const ctx = await extractContext(content);
      setContext(ctx);

      setStep("Generating blog post & social content...");
      const [blogResult, linkedInResult, threadResult, socialResult] = await Promise.all([
        generateBlog(content, ctx),
        generateLinkedIn(content, ctx),
        generateTwitterThread(content, ctx),
        generateContent(content),
      ]);

      setBlog(blogResult);
      setLinkedIn(linkedInResult);
      setThread(threadResult);
      setOutput(socialResult);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Something went wrong.");
    } finally {
      setLoading(false);
      setStep("");
    }
  }

  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <div style={styles.badge}>AI Powered</div>
        <h1 style={styles.title}>AI Context Repurposing Agent</h1>
        <p style={styles.subtitle}>
          Turn any YouTube video, blog post, or audio into blog articles, LinkedIn posts, Twitter threads, and more.
        </p>
      </header>

      <main style={styles.main}>
        {/* Backend status banners */}
        {backendStatus === "checking" && (
          <div style={{ ...styles.banner, ...styles.bannerInfo }}>⏳ Connecting to backend...</div>
        )}
        {backendStatus === "down" && (
          <div style={{ ...styles.banner, ...styles.bannerError }}>
            ❌ Backend is not running. Start it with:<br />
            <code style={styles.code}>cd ai-context-agent/backend &amp;&amp; venv\Scripts\uvicorn main:app --reload --port 8000</code>
          </div>
        )}
        {backendStatus === "no-key" && (
          <div style={{ ...styles.banner, ...styles.bannerWarn }}>
            ⚠️ OpenAI API key is missing. Edit <code style={styles.code}>backend/.env</code> and set <code style={styles.code}>OPENAI_API_KEY=sk-...</code>, then restart the server.
          </div>
        )}

        <section style={styles.card}>
          <h2 style={styles.sectionTitle}>Input Content</h2>
          <InputForm onSubmit={handleSubmit} loading={loading} />
          {loading && <p style={styles.status}>{step}</p>}
          {error && <p style={styles.error}>{error}</p>}
        </section>

        {context && (
          <section style={styles.card}>
            <h2 style={styles.sectionTitle}>Content Analysis</h2>
            <ContextPanel data={context} />
          </section>
        )}

        {blog && (
          <section style={styles.card}>
            <h2 style={styles.sectionTitle}>Blog Post</h2>
            <BlogPreview data={blog} />
          </section>
        )}

        {linkedIn && (
          <section style={styles.card}>
            <h2 style={styles.sectionTitle}>LinkedIn Post</h2>
            <LinkedInPreview data={linkedIn} />
          </section>
        )}

        {thread && (
          <section style={styles.card}>
            <h2 style={styles.sectionTitle}>Twitter Thread</h2>
            <TwitterThread data={thread} />
          </section>
        )}

        {output && (
          <section style={styles.card}>
            <h2 style={styles.sectionTitle}>Social & Other Formats</h2>
            <OutputTabs data={output} />
          </section>
        )}
      </main>
    </div>
  );
}

const styles = {
  page: { minHeight: "100vh", padding: "2rem 1rem" },
  header: { textAlign: "center", marginBottom: "2.5rem" },
  badge: {
    display: "inline-block",
    padding: "0.3rem 0.9rem",
    borderRadius: "999px",
    background: "rgba(79,70,229,0.15)",
    border: "1px solid rgba(79,70,229,0.4)",
    color: "#a5b4fc",
    fontSize: "0.75rem",
    fontWeight: "600",
    letterSpacing: "0.05em",
    marginBottom: "1rem",
    textTransform: "uppercase",
  },
  title: {
    fontSize: "clamp(1.75rem, 4vw, 2.75rem)",
    fontWeight: "700",
    background: "linear-gradient(135deg, #a5b4fc, #7c3aed)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    marginBottom: "0.75rem",
  },
  subtitle: { color: "#64748b", fontSize: "1rem", maxWidth: "520px", margin: "0 auto" },
  main: {
    maxWidth: "860px",
    margin: "0 auto",
    display: "flex",
    flexDirection: "column",
    gap: "1.5rem",
  },
  card: {
    background: "#13131f",
    border: "1px solid #2d2d44",
    borderRadius: "16px",
    padding: "1.75rem",
  },
  sectionTitle: {
    fontSize: "1rem",
    fontWeight: "600",
    color: "#94a3b8",
    marginBottom: "1.25rem",
    textTransform: "uppercase",
    letterSpacing: "0.05em",
  },
  status: { marginTop: "1rem", color: "#a5b4fc", fontSize: "0.9rem", textAlign: "center" },
  error: {
    marginTop: "1rem",
    color: "#f87171",
    fontSize: "0.9rem",
    background: "rgba(248,113,113,0.08)",
    padding: "0.75rem 1rem",
    borderRadius: "8px",
    border: "1px solid rgba(248,113,113,0.2)",
  },
  banner: {
    padding: "0.85rem 1.25rem",
    borderRadius: "10px",
    fontSize: "0.875rem",
    lineHeight: "1.6",
  },
  bannerInfo: {
    background: "rgba(99,102,241,0.08)",
    border: "1px solid rgba(99,102,241,0.25)",
    color: "#a5b4fc",
  },
  bannerError: {
    background: "rgba(248,113,113,0.08)",
    border: "1px solid rgba(248,113,113,0.3)",
    color: "#fca5a5",
  },
  bannerWarn: {
    background: "rgba(245,158,11,0.08)",
    border: "1px solid rgba(245,158,11,0.3)",
    color: "#fcd34d",
  },
  code: {
    fontFamily: "monospace",
    background: "rgba(0,0,0,0.3)",
    padding: "0.1rem 0.4rem",
    borderRadius: "4px",
    fontSize: "0.8rem",
  },
};
