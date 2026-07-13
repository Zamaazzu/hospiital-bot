// Generates public/greeting.wav from GREETING_TEXT by calling the backend's
// /tts endpoint ONCE and saving the audio to disk as a static asset.
//
// Why: GREETING_TEXT never changes, so there's no reason to make the user
// wait on a live Sarvam TTS synthesis call every time they tap the mic.
// VoiceBot.jsx plays this static file directly; it only falls back to a
// live TTS call if this file is missing.
//
// Run this once now, and again any time GREETING_TEXT changes:
//
//   node scripts/generate-greeting.mjs
//
// Uses the same backend URL your dev server proxies to (VITE_BACKEND_URL
// in your root .env, falling back to http://192.168.1.22:8000 — matches
// vite.config.js).

import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { GREETING_TEXT } from "../src/constants/departments.js";

const BACKEND_URL = process.env.VITE_BACKEND_URL || "http://192.168.1.22:8000";
const OUT_PATH = path.join(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
  "public",
  "greeting.wav"
);

async function main() {
  console.log(`Requesting TTS from ${BACKEND_URL}/tts ...`);
  const res = await fetch(`${BACKEND_URL}/tts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: GREETING_TEXT }),
  });

  if (!res.ok) {
    throw new Error(`TTS request failed: ${res.status} ${await res.text()}`);
  }

  const data = await res.json();
  if (!data.audio_base64) {
    throw new Error(
      "Response had no audio_base64 field. Backend /tts must return " +
        "{ audio_base64 } (see api.js textToSpeech note)."
    );
  }

  await writeFile(OUT_PATH, Buffer.from(data.audio_base64, "base64"));
  console.log(`Saved greeting audio to ${OUT_PATH}`);
}

main().catch((err) => {
  console.error("Failed to generate greeting audio:", err.message);
  process.exit(1);
});
