import { useState, useEffect, useRef } from "react";

/**
 * Wraps the browser's Web Speech API (SpeechRecognition) into continuous
 * listening while `isListening` is true. Returns the accumulated final
 * transcript, the current interim (not-yet-final) transcript, whether the
 * browser supports it at all, and any error code encountered.
 */
export function useSpeechToText(isListening) {
  const [transcript, setTranscript] = useState("");
  const [interimTranscript, setInterimTranscript] = useState("");
  const [supported, setSupported] = useState(true);
  const [error, setError] = useState(null);
  const recognitionRef = useRef(null);
  const shouldRunRef = useRef(false);

  useEffect(() => {
    const SpeechRecognitionClass =
      typeof window !== "undefined" && (window.SpeechRecognition || window.webkitSpeechRecognition);

    if (!SpeechRecognitionClass) {
      setSupported(false);
      return;
    }

    if (!isListening) {
      shouldRunRef.current = false;
      if (recognitionRef.current) {
        recognitionRef.current.onend = null;
        recognitionRef.current.stop();
        recognitionRef.current = null;
      }
      setInterimTranscript("");
      return;
    }

    shouldRunRef.current = true;
    setTranscript("");
    setInterimTranscript("");
    setError(null);

    const recognition = new SpeechRecognitionClass();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-IN";

    recognition.onresult = (event) => {
      let interim = "";
      let final = "";
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const text = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          final += text;
        } else {
          interim += text;
        }
      }
      if (final.trim()) {
        setTranscript((prev) => (prev ? `${prev} ${final.trim()}` : final.trim()));
      }
      setInterimTranscript(interim);
    };

    recognition.onerror = (event) => {
      // "no-speech" fires constantly during natural pauses — not a real error
      if (event.error === "no-speech" || event.error === "aborted") return;
      setError(event.error);
      if (event.error === "not-allowed" || event.error === "service-not-allowed") {
        shouldRunRef.current = false;
      }
    };

    recognition.onend = () => {
      // Some browsers end recognition after a pause; restart while still listening
      if (shouldRunRef.current) {
        try {
          recognition.start();
        } catch (e) {
          // already started
        }
      }
    };

    recognitionRef.current = recognition;
    try {
      recognition.start();
    } catch (e) {
      setError(e && e.message ? e.message : "start-failed");
    }

    return () => {
      shouldRunRef.current = false;
      recognition.onend = null;
      recognition.stop();
      if (recognitionRef.current === recognition) recognitionRef.current = null;
    };
  }, [isListening]);

  return { transcript, interimTranscript, supported, error };
}
