import React, { useEffect } from "react";
import { Mic } from "lucide-react";
import { useWaveform } from "../../hooks/useWaveform";
import { useSpeechToText } from "../../hooks/useSpeechToText";
import { BAR_COUNT, GREETING_TEXT } from "../../constants/departments";

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
 * microphone. Owns both the audio-level hook and the speech-to-text hook.
 *
 * Reports the recognized transcript upward via `onTranscript` so the parent
 * can drive voice navigation (e.g. opening a department when its name is
 * spoken) without VoiceBot needing to know about departments at all.
 */
export default function VoiceBot({ isListening, onToggle, onTranscript }) {
  const bars = useWaveform(isListening);
  const { transcript, interimTranscript, supported: speechSupported, error: speechError } =
    useSpeechToText(isListening);

  useEffect(() => {
    if (onTranscript) onTranscript(transcript);
  }, [transcript, onTranscript]);

  useEffect(() => {
    if (typeof window === "undefined" || !window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    if (!isListening) return;
    try {
      const utter = new SpeechSynthesisUtterance(GREETING_TEXT);
      utter.rate = 1;
      utter.pitch = 1.02;
      window.speechSynthesis.speak(utter);
    } catch (e) {
      // speech synthesis unavailable — bubble text still shows
    }
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

      <div style={styles.micLabel}>{isListening ? "Listening…" : "Press & speak"}</div>
      <div style={styles.micSub}>
        {isListening ? "Tap the mic to stop" : "Tap the microphone and speak"}
      </div>

      {isListening && (
        <div style={styles.transcriptBox} className="hvb-fade-in">
          {!speechSupported ? (
            <span style={styles.transcriptPlaceholder}>
              Voice input isn't supported in this browser — try Chrome or Edge.
            </span>
          ) : speechError === "not-allowed" || speechError === "service-not-allowed" ? (
            <span style={styles.transcriptError}>
              Microphone access was blocked. Please allow microphone permission for this page
              (check the site/lock icon in your address bar) and tap the mic again.
            </span>
          ) : speechError ? (
            <span style={styles.transcriptError}>
              Voice recognition hit an error ({speechError}). Tap the mic to try again.
            </span>
          ) : transcript || interimTranscript ? (
            <span>
              {transcript}
              {interimTranscript && <span style={styles.transcriptInterim}> {interimTranscript}</span>}
            </span>
          ) : (
            <span style={styles.transcriptPlaceholder}>Say a department name, e.g. "Cardiology"…</span>
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
