import { useRef, useCallback } from "react";

// The backend reads uploaded audio as-is via soundfile, so we must produce a
// real WAV file in the browser (MediaRecorder alone can't do this — Chrome
// only outputs webm/opus, which soundfile can't decode).
function encodeWAV(samples, sampleRate) {
  const buffer = new ArrayBuffer(44 + samples.length * 2);
  const view = new DataView(buffer);

  const writeString = (offset, str) => {
    for (let i = 0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i));
  };

  writeString(0, "RIFF");
  view.setUint32(4, 36 + samples.length * 2, true);
  writeString(8, "WAVE");
  writeString(12, "fmt ");
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 1, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);
  writeString(36, "data");
  view.setUint32(40, samples.length * 2, true);

  let offset = 44;
  for (let i = 0; i < samples.length; i++, offset += 2) {
    const s = Math.max(-1, Math.min(1, samples[i]));
    view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
  }

  return new Blob([view], { type: "audio/wav" });
}

export function useAudioRecorder() {
  const audioCtxRef = useRef(null);
  const processorRef = useRef(null);
  const sourceRef = useRef(null);
  const chunksRef = useRef([]);
  const sampleRateRef = useRef(16000);

  // Takes the already-open mic stream (acquired once in VoiceBot and shared
  // with the waveform visualizer) instead of calling getUserMedia itself —
  // avoids opening a second, possibly-silent capture stream on top of the
  // one already in use.
  const start = useCallback(async (stream) => {
    if (!stream) throw new Error("No microphone stream available");

    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    const audioCtx = new AudioContextClass();
    audioCtxRef.current = audioCtx;
    sampleRateRef.current = audioCtx.sampleRate;

    // AudioContexts can be created in a "suspended" state — especially
    // likely here since this runs after an `await` (the greeting playback),
    // by which point the browser may no longer count this as a fresh user
    // gesture. Left suspended, onaudioprocess never fires and the recording
    // is silence with no error raised anywhere. Explicitly resuming makes
    // sure audio actually flows.
    if (audioCtx.state === "suspended") {
      await audioCtx.resume();
    }

    const source = audioCtx.createMediaStreamSource(stream);
    sourceRef.current = source;

    const processor = audioCtx.createScriptProcessor(4096, 1, 1);
    processorRef.current = processor;
    chunksRef.current = [];

    processor.onaudioprocess = (e) => {
      chunksRef.current.push(new Float32Array(e.inputBuffer.getChannelData(0)));
    };

    source.connect(processor);
    processor.connect(audioCtx.destination);
  }, []);

  const stop = useCallback(() => {
    return new Promise((resolve) => {
      processorRef.current?.disconnect();
      sourceRef.current?.disconnect();
      audioCtxRef.current?.close().catch(() => {});

      const totalLength = chunksRef.current.reduce((sum, c) => sum + c.length, 0);
      const merged = new Float32Array(totalLength);
      let offset = 0;
      for (const chunk of chunksRef.current) {
        merged.set(chunk, offset);
        offset += chunk.length;
      }

      const wavBlob = encodeWAV(merged, sampleRateRef.current);
      resolve(wavBlob);
    });
  }, []);

  return { start, stop };
}
