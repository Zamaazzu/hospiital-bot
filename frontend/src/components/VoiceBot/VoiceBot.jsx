import React, { useEffect, useRef, useState } from "react";
import { Mic } from "lucide-react";
import { useWaveform } from "../../hooks/useWaveform";
import { useAudioRecorder } from "../../hooks/useAudioRecorder";
import { sendVoiceMessage, textToSpeech } from "../../services/api";
import { BAR_COUNT, GREETING_TEXT } from "../../constants/departments";

// Pre-rendered greeting clip, served as a static asset from /public.
// Generate/refresh it with `node scripts/generate-greeting.mjs` (see
// scripts/generate-greeting.mjs) whenever GREETING_TEXT changes.
const GREETING_AUDIO_URL = "/greeting.wav";

function PlasmaFace({ active }) {
  return (
    <span className={`hvb-mic-face ${active ? "hvb-mic-face-active" : ""}`}>
      <span className="hvb-plasma-highlight" style={{ opacity: active ? 0.7 : 0 }} />
      <span className="hvb-plasma-sheen" />
    </span>
  );
}

function SiriBlobOverlay({ active, bars }) {
  const avg = bars && bars.length ? bars.reduce((a, v) => a + v, 0) / bars.length : 12;
  const level = Math.max(0.15, Math.min(1, (avg - 5) / 26));

  return (
    <span className={`hvb-siri-blobs-wrap ${active ? "hvb-siri-blobs-active" : ""}`}>
      <span
        className="hvb-siri-level"
        style={{ transform: `scale(${(1 + level * 0.16).toFixed(3)})` }}
      >
        <span className="hvb-siri-blob hvb-siri-blob-blue" />
        <span className="hvb-siri-blob hvb-siri-blob-green" />
        <span className="hvb-siri-blob hvb-siri-blob-pink" />
        <span className="hvb-siri-blob hvb-siri-blob-purple" />
        <span className="hvb-siri-core" style={{ opacity: 0.6 + level * 0.4 }} />
      </span>
    </span>
  );
}

const styles = {
  micWrap: {
    position: "relative",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 2,
    height: "130px",
  },
  micButton: {
    position: "relative",
    width: 118,
    height: 118,
    borderRadius: "50%",
    background: "none",
    border: "none",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    cursor: "pointer",
    overflow: "visible",
  },
  micLabel: {
    position: "relative",
    zIndex: 1,
    fontFamily: "'Sora', sans-serif",
    fontWeight: 700,
    fontSize: "16.5px",
    color: "#6A3FD6",
    marginTop: "6px",
    letterSpacing: "0.2px",
  },
  micSub: {
    position: "relative",
    zIndex: 1,
    fontSize: "13px",
    color: "#9C8FBE",
    marginTop: "4px",
    marginBottom: "20px",
  },
  transcriptBox: {
    position: "relative",
    zIndex: 1,
    maxWidth: "460px",
    margin: "0 auto 18px",
    padding: "10px 18px",
    borderRadius: "14px",
    background: "#FBF8FF",
    border: "1px solid #EADFFF",
    fontSize: "13.5px",
    color: "#3E2E5C",
    lineHeight: 1.5,
    minHeight: "20px",
  },
  transcriptInterim: { color: "#B3A4D6" },
  transcriptPlaceholder: { color: "#B3A4D6", fontStyle: "italic" },
  transcriptError: { color: "#C0392B" },
  waveRow: {
    position: "relative",
    zIndex: 1,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "3px",
    height: "44px",
  },
};

/**
 * Self-contained voice interaction module: mic button + Siri-style listening
 * animation + live transcript box + waveform bars driven by the real
 * microphone. Owns both the audio-level hook and the voice hook.
 *
 * Reports the bot's spoken reply upward via `onReply` so the parent can show
 * it in the conversation bubble (see Conversation.jsx's `message` prop).
 *
 * The greeting only plays once per "session" — the first mic tap after
 * mount, or after `greetingResetKey` changes (the parent bumps this when a
 * token booking completes, so the next person gets greeted fresh).
 */
export default function VoiceBot({ isListening, onToggle, onReply, greetingResetKey }) {
  // True only while the greeting is being spoken — the mic must stay
  // deaf during this, so it can't pick up the bot's own voice or the
  // user talking over it.
  const [isGreeting, setIsGreeting] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [botReply, setBotReply] = useState("");
  // Department the backend resolved from the spoken request (if any) —
  // { id, name } or null. Reported upward alongside the reply text so the
  // parent can auto-open that department instead of just showing text.
  const [departmentMatch, setDepartmentMatch] = useState(null);
  const [speechError, setSpeechError] = useState(null);
  const speechSupported =
    typeof navigator !== "undefined" && !!navigator.mediaDevices?.getUserMedia;

  const { start: startRecording, stop: stopRecording } = useAudioRecorder();
  const greetingAudioRef = useRef(null);
  // In-memory cache for the fallback (live TTS) greeting audio, so that if
  // /greeting.wav is ever missing we still only pay the network+synthesis
  // cost once per page load, not once per mic click.
  const liveGreetingCacheRef = useRef(null);
  // Tracks whether the greeting has already played this session. Starts
  // false so the very first tap greets; stays true afterward so repeated
  // taps skip straight to listening — until a booking completes and resets
  // it (see the greetingResetKey effect below), for the next person.
  const hasGreetedRef = useRef(false);

  const bars = useWaveform(isListening);

  useEffect(() => {
    if (onReply) onReply(botReply, departmentMatch, isGreeting);
  }, [botReply, departmentMatch, isGreeting, onReply]);

  // Bumped by the parent whenever a token booking completes — allow the
  // greeting to play again on the next mic tap, for the next person.
  useEffect(() => {
    hasGreetedRef.current = false;
  }, [greetingResetKey]);

  // Single sequential flow, triggered only by isListening:
  //   1. Attempt the Malayalam greeting (Sarvam TTS) and wait for it to finish
  //      — but only if it hasn't already played this session.
  //   2. Start recording real WAV audio for the backend's Malayalam STT.
  //   3. When isListening flips back to false, the cleanup below stops the
  //      recording and sends it to /voice for transcription + reply + TTS.
  // Doing this as one effect (instead of two effects reacting to each
  // other's state) avoids a race where recording could start and get
  // stopped again before the user had a chance to speak.
  useEffect(() => {
    if (!isListening) return;

    let cancelled = false;
    let recordingStarted = false;

    setBotReply("");
    setDepartmentMatch(null);
    setSpeechError(null);
    setIsGreeting(true);

    (async () => {
      // Only play the greeting once per session — repeated mic taps skip it
      // until a booking completes and resets hasGreetedRef (see above).
      if (!hasGreetedRef.current) {
        hasGreetedRef.current = true;

        // 1. Try the pre-rendered static greeting first (see
        //    public/greeting.wav / scripts/generate-greeting.mjs). Since
        //    GREETING_TEXT never changes, there's no reason to hit the TTS
        //    API and wait on synthesis for every mic click — this plays
        //    near-instantly straight from disk/CDN.
        const playedStatic = await new Promise((resolve) => {
          const audio = new Audio(GREETING_AUDIO_URL);
          greetingAudioRef.current = audio;
          audio.onended = () => resolve(true);
          audio.onerror = () => resolve(false);
          audio.play().then(() => {}).catch(() => resolve(false));
        });

        // 2. Fall back to live TTS only if the static file is missing/broken
        //    (e.g. it hasn't been generated yet). Cache the result so this
        //    slow path only ever runs once per page load, not once per click.
        if (!playedStatic && !cancelled) {
          try {
            if (!liveGreetingCacheRef.current) {
              liveGreetingCacheRef.current = await textToSpeech(GREETING_TEXT);
            }
            const result = liveGreetingCacheRef.current;
            if (!cancelled && result?.audio_base64) {
              await new Promise((resolve) => {
                const audio = new Audio(`data:audio/wav;base64,${result.audio_base64}`);
                greetingAudioRef.current = audio;
                audio.onended = resolve;
                audio.onerror = resolve;
                audio.play().catch(resolve);
              });
            }
          } catch (e) {
            // Greeting failed — fine, proceed straight to listening.
          }
        }
      }

      if (cancelled) return;
      setIsGreeting(false);

      try {
        await startRecording();
        recordingStarted = true;
      } catch (e) {
        if (!cancelled) {
          setSpeechError(e?.message === "Permission denied" ? "not-allowed" : "start-failed");
        }
      }
    })();

    return () => {
      cancelled = true;
      setIsGreeting(false); // reset immediately so a mid-greeting tap returns to "Press & speak", not a stuck "Speaking…"
      if (greetingAudioRef.current) {
        greetingAudioRef.current.pause();
        greetingAudioRef.current = null;
      }
      if (recordingStarted) {
        setIsTranscribing(true);
        stopRecording()
          .then((wavBlob) => sendVoiceMessage(wavBlob))
          .then((result) => {
            setBotReply(result.reply_text || "");
            setDepartmentMatch(
              result.department_id
                ? { id: result.department_id, name: result.department_name }
                : null
            );
            if (result.audio_base64) {
              const audio = new Audio(`data:audio/wav;base64,${result.audio_base64}`);
              audio.play().catch(() => {});
            }
          })
          .catch(() => setSpeechError("transcription-failed"))
          .finally(() => setIsTranscribing(false));
      }
    };
  }, [isListening]);

  return (
    <>
      <div style={styles.micWrap}>
        <div className="hvb-sonar-track">
          <span className={`hvb-sonar ${isListening ? "hvb-sonar-active" : ""}`} />
          <span className={`hvb-sonar hvb-sonar-2 ${isListening ? "hvb-sonar-active" : ""}`} />
        </div>
        <button
          aria-pressed={isListening}
          aria-label={isListening ? "Stop listening" : "Start listening"}
          onClick={onToggle}
          style={styles.micButton}
          className={`hvb-mic-btn ${isListening ? "hvb-mic-on" : ""}`}
        >
          <PlasmaFace active={isListening} />
          <span
            className="hvb-mic-icon-layer"
            style={{ opacity: isListening ? 0 : 1, transform: isListening ? "scale(0.7)" : "scale(1)" }}
          >
            <Mic size={40} color="#fff" strokeWidth={2.2} />
          </span>
          <SiriBlobOverlay active={isListening} bars={bars} />
        </button>
      </div>

      <div style={styles.micLabel}>
        {isGreeting
          ? "Speaking…"
          : isTranscribing
          ? "Processing…"
          : isListening
          ? "Listening…"
          : "Press & speak"}
      </div>
      <div style={styles.micSub}>
        {isGreeting
          ? "One moment, please…"
          : isTranscribing
          ? "Understanding what you said…"
          : isListening
          ? "Tap the mic to stop"
          : "Tap the microphone and speak"}
      </div>

      {(isListening || isTranscribing) && !isGreeting && (
        <div style={styles.transcriptBox} className="hvb-fade-in">
          {!speechSupported ? (
            <span style={styles.transcriptPlaceholder}>
              Voice input isn't supported in this browser — microphone access is required.
            </span>
          ) : speechError === "not-allowed" ? (
            <span style={styles.transcriptError}>
              Microphone access was blocked. Please allow microphone permission for this page
              (check the site/lock icon in your address bar) and tap the mic again.
            </span>
          ) : speechError ? (
            <span style={styles.transcriptError}>
              Voice recognition hit an error ({speechError}). Tap the mic to try again.
            </span>
          ) : botReply ? (
            <span>{botReply}</span>
          ) : isTranscribing ? (
            <span style={styles.transcriptPlaceholder}>Processing…</span>
          ) : (
            <span style={styles.transcriptPlaceholder}>സംസാരിക്കൂ…</span>
          )}
        </div>
      )}

      <div style={styles.waveRow} className="hvb-wave-row">
        {bars.map((h, i) => (
          <span
            key={i}
            className="hvb-bar"
            style={{
              height: `${h}px`,
              background: Math.abs(i - BAR_COUNT / 2) < 2 ? "#8A5AE5" : "rgba(138,90,229,0.55)",
              opacity: isListening ? 1 : 0.3,
            }}
          />
        ))}
      </div>
    </>
  );
}
