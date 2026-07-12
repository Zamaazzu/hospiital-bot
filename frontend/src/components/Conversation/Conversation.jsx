import React from "react";
import { Bot } from "lucide-react";
import { GREETING_TEXT } from "../../constants/departments";

const styles = {
  botBubble: {
    position: "relative",
    zIndex: 1,
    display: "flex",
    alignItems: "flex-start",
    gap: "10px",
    textAlign: "left",
    background: "#fff",
    border: "1px solid #DCCEFF",
    borderRadius: "18px",
    padding: "12px 16px 14px",
    marginTop: "10px",
    marginBottom: "22px",
    maxWidth: "360px",
    marginLeft: "auto",
    marginRight: "auto",
    boxShadow: "0 10px 24px -10px rgba(106,63,214,0.2)",
  },
  botAvatar: {
    width: 26,
    height: 26,
    borderRadius: "50%",
    background: "linear-gradient(150deg, #B86FEA, #6A3FD6)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
    marginTop: "1px",
  },
  botBubbleText: {
    margin: 0,
    fontSize: "13.5px",
    color: "#4B3B66",
    lineHeight: 1.5,
  },
  heroSubtitle: {
    position: "relative",
    zIndex: 1,
    fontSize: "14px",
    color: "#8577A0",
    marginTop: "8px",
    marginBottom: "20px",
    maxWidth: "380px",
    marginLeft: "auto",
    marginRight: "auto",
    lineHeight: 1.5,
  },
};

/**
 * Shows the assistant's greeting bubble while listening, or a short
 * instructional subtitle otherwise. This is the seam where Person 3/4's
 * real intent + reply text (from /chat) should eventually replace the
 * static GREETING_TEXT.
 */
export default function Conversation({ isListening, message = GREETING_TEXT }) {
  if (isListening) {
    return (
      <div key="bubble" style={styles.botBubble} className="hvb-bot-bubble">
        <span style={styles.botAvatar} className="hvb-bot-avatar">
          <Bot size={15} color="#fff" />
        </span>
        <p style={styles.botBubbleText}>{message}</p>
        <span className="hvb-bot-bubble-tail" />
      </div>
    );
  }

  return (
    <p key="subtitle" style={styles.heroSubtitle}>
     നിങ്ങളുടെ ശബ്ദം മതി — അപ്പോയിന്റ്മെന്റ് മുതൽ ക്യൂ വരെ, എല്ലാം എളുപ്പമായി.
    </p>
  );
}
