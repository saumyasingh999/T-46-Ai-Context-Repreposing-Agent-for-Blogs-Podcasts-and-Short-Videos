import axios from "axios";

const BASE = "http://127.0.0.1:8000";

const client = axios.create({ baseURL: BASE });

// ── Response interceptor: surface meaningful errors ──────────────────────────
client.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.code === "ERR_NETWORK" || err.code === "ECONNREFUSED") {
      return Promise.reject(
        new Error("Cannot reach the backend. Make sure the FastAPI server is running on port 8000.")
      );
    }
    const detail = err.response?.data?.detail;
    if (detail) {
      return Promise.reject(new Error(Array.isArray(detail) ? detail[0]?.msg : detail));
    }
    return Promise.reject(new Error(err.message || "Unknown error"));
  }
);

export async function checkHealth() {
  const { data } = await client.get("/health");
  return data;
}

export async function ingestContent({ youtubeUrl, blogText, audioFile }) {
  const form = new FormData();
  if (youtubeUrl) form.append("youtube_url", youtubeUrl);
  if (blogText)   form.append("blog_text",   blogText);
  if (audioFile)  form.append("audio_file",  audioFile);
  const { data } = await client.post("/ingest/", form);
  return data.content;
}

export async function extractContext(content) {
  const { data } = await client.post("/extract/", { content });
  return data;
}

export async function generateBlog(content, context) {
  const { data } = await client.post("/blog/", { content, context });
  return data;
}

export async function generateLinkedIn(content, context) {
  const { data } = await client.post("/linkedin/", { content, context });
  return data;
}

export async function generateTwitterThread(content, context) {
  const { data } = await client.post("/twitter/", { content, context });
  return data;
}

export async function generateContent(content) {
  const { data } = await client.post("/generate/", { content });
  return data;
}
