import { useState, useEffect, useRef } from "react";
import { BAR_COUNT, STATIC_BAR_HEIGHT, SILENCE_THRESHOLD } from "../constants/departments";

/**
 * Drives the waveform bars from the real microphone via an AnalyserNode.
 * Takes the already-open mic stream (acquired once in VoiceBot) rather than
 * calling getUserMedia itself, so it isn't competing with the recorder for
 * a second capture stream on the same device. Falls back to a flat static
 * wave if no stream is available yet, or while the input is silent.
 */
export function useWaveform(isListening, stream) {
  const [bars, setBars] = useState(() => Array.from({ length: BAR_COUNT }, () => STATIC_BAR_HEIGHT));
  const audioCtxRef = useRef(null);
  const analyserRef = useRef(null);
  const rafRef = useRef(null);
  const dataArrayRef = useRef(null);

  useEffect(() => {
    let cancelled = false;

    const toStatic = () => setBars(Array.from({ length: BAR_COUNT }, () => STATIC_BAR_HEIGHT));

    function stop() {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
      if (audioCtxRef.current) {
        audioCtxRef.current.close().catch(() => {});
        audioCtxRef.current = null;
      }
      analyserRef.current = null;
      dataArrayRef.current = null;
      toStatic();
    }

    async function start() {
      try {
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        const audioCtx = new AudioContextClass();
        audioCtxRef.current = audioCtx;

        // See useAudioRecorder for why this matters: a freshly created
        // AudioContext can start "suspended" and never actually process
        // audio, silently leaving the visualization (and, there, the
        // recording) dead with no error.
        if (audioCtx.state === "suspended") {
          await audioCtx.resume();
        }
        if (cancelled) return;

        const source = audioCtx.createMediaStreamSource(stream);
        const analyser = audioCtx.createAnalyser();
        analyser.fftSize = 256;
        analyser.smoothingTimeConstant = 0.75;
        source.connect(analyser);
        analyserRef.current = analyser;

        const data = new Uint8Array(analyser.frequencyBinCount);
        dataArrayRef.current = data;

        const tick = () => {
          if (!analyserRef.current || !dataArrayRef.current) return;
          analyserRef.current.getByteFrequencyData(dataArrayRef.current);

          const avg = dataArrayRef.current.reduce((a, v) => a + v, 0) / dataArrayRef.current.length;

          if (avg < SILENCE_THRESHOLD) {
            // no real voice input right now — keep the wave flat
            toStatic();
          } else {
            setBars(
              Array.from({ length: BAR_COUNT }, (_, i) => {
                const dataIndex = Math.floor((i / BAR_COUNT) * dataArrayRef.current.length);
                const value = dataArrayRef.current[dataIndex] || 0;
                const centerBoost = 1 - Math.abs(i - BAR_COUNT / 2) / (BAR_COUNT / 2);
                const height = STATIC_BAR_HEIGHT + (value / 255) * 34 * (0.5 + centerBoost * 0.5);
                return Math.max(4, height);
              })
            );
          }

          rafRef.current = requestAnimationFrame(tick);
        };

        tick();
      } catch (err) {
        // AudioContext/analyser setup failed — fall back to a static wave
        toStatic();
      }
    }

    if (isListening && stream) {
      start();
    } else {
      stop();
    }

    return () => {
      cancelled = true;
      stop();
    };
  }, [isListening, stream]);

  return bars;
}
