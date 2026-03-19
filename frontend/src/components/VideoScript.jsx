import { useState } from "react";

const TECHNIQUE_COLORS = {
  stat:          { color: "#f59e0b", bg: "rgba(245,158,11,0.1)"  },
  story:         { color: "#a78bfa", bg: "rgba(167,139,250,0.1)" },
  demonstration: { color: "#34d399", bg: "rgba(52,211,153,0.1)"  },
  contrast:      { color: "#f87171", bg: "rgba(248,113,113,0.1)" },
  question:      { color: "#60a5fa", bg: "rgba(96,165,250,0.1)"  },
};

const ACTION_ICONS = {
  follow: "👤", "link in bio": "🔗", comment: "💬", share: "📤", save: "🔖",
};

function TimingBar({ seconds, total }) {
  const pct = (seconds / total) * 