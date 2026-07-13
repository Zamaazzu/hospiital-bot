import { useState, useEffect, useRef } from "react";
import { BAR_COUNT, STATIC_BAR_HEIGHT, SILENCE_THRESHOLD } from "../constants/departments";

/**
 * Drives the waveform bars from the real microphone via getUserMedia +
 * AnalyserNode. Falls back to a flat static wave if mic permission is
 * denied/unavailable, or while the input is silent.
 */
export function useWaveform(isListening) {
  const [bars, setBars] = useState(() => Array.from({ length: BAR_COUNT }, () => STATIC_BAR_HEIGHT));
  const audioCtxRef = useRef(null);
  const analyserRef = useRef(null);
  const streamRef = useRef(null);
  const rafRef = useRef(null);
  const dataArrayRef = useRef(null);

  useEffect(() => {
    let cancelled = false;

    const toStatic = () => setBars(Array.from({ length: BAR_COUNT }, () => STATIC_BAR_HEIGHT));

    function stop() {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((t) => t.stop());
        streamRef.current = null;
      }
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
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        if (cancelled) {
          stream.getTracks().forEach((t) => t.stop());
          return;
        }
        streamRef.current = stream;

        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        const audioCtx = new AudioContextClass();
        audioCtxRef.current = audioCtx;

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
        // mic permission denied or unavailable — fall back to a static wave
        toStatic();
      }
    }

    if (isListening) {
      start();
    } else {
      stop();
    }

    return () => {
      cancelled = true;
      stop();
    };
  }, [isListening]);

  return bars;
}
