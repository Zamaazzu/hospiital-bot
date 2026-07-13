import React from "react";
import { Stethoscope, Plus } from "lucide-react";
import Conversation from "../Conversation/Conversation";
import VoiceBot from "../VoiceBot/VoiceBot";

const styles = {
  hero: {
    position: "relative",
    overflow: "hidden",
    background: "transparent",
    border: "none",
    borderRadius: "0px",
    padding: "10px 24px 20px",
    textAlign: "center",
    marginBottom: "0px",
    boxShadow: "none",
    flex: "1 1 auto",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    minHeight: 0,
  },
  heroTopRow: {
    position: "relative",
    zIndex: 1,
    display: "flex",
    justifyContent: "center",
    marginBottom: "10px",
  },
  heroEyebrow: {
    display: "inline-block",
    fontSize: "11.5px",
    fontWeight: 700,
    letterSpacing: "1.6px",
    textTransform: "uppercase",
    color: "#8A5AE5",
    background: "#F1E4FD",
    padding: "6px 14px",
    borderRadius: "999px",
  },
  heroActionBtn: {
    position: "absolute",
    right: "22px",
    zIndex: 3,
    display: "flex",
    alignItems: "center",
    gap: "7px",
    background: "#fff",
    color: "#6D42D8",
    border: "1px solid #DCCEFF",
    borderRadius: "16px",
    padding: "9px 15px",
    fontSize: "12px",
    fontWeight: 700,
    letterSpacing: "0.2px",
    cursor: "pointer",
    boxShadow: "0 6px 20px rgba(122,80,220,.15)",
  },
};

export default function Hero({
  isListening,
  onToggleListening,
  botReply,
  onReply,
  showDoctors,
  onOpenDoctors,
  onOpenGeneralOp,
}) {
  return (
    <section style={styles.hero} className="hvb-fade-in hvb-delay-1">
      <div className="hvb-blob hvb-blob-a" />
      <div className="hvb-blob hvb-blob-b" />
      <div className="hvb-grid-pattern" />

      <div style={styles.heroTopRow}>
        <span style={styles.heroEyebrow}>AI Front Desk</span>
      </div>

      <button
        onClick={onOpenDoctors}
        style={{ ...styles.heroActionBtn, top: "58px" }}
        className="hvb-hero-doctors-btn"
        aria-haspopup="dialog"
        aria-expanded={showDoctors}
      >
        <Stethoscope size={15} />
        <span>Today's Doctors</span>
      </button>

      <button
        onClick={onOpenGeneralOp}
        style={{ ...styles.heroActionBtn, top: "102px" }}
        className="hvb-hero-doctors-btn"
      >
        <Plus size={15} />
        <span>General OP</span>
      </button>

      <Conversation isListening={isListening} message={botReply || undefined} />

      <VoiceBot isListening={isListening} onToggle={onToggleListening} onReply={onReply} />
    </section>
  );
}
