import React from "react";
import { Calendar } from "lucide-react";
import hospitalLogo from "../../assets/hospital-logo-icon.png";

const styles = {
  header: {
    position: "relative",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "6px 4px 14px",
    flexShrink: 0,
  },
  logoRow: { display: "flex", alignItems: "center", justifyContent: "center", gap: "15px" },
  logoBadge: {
    width: 54,
    height: 54,
    borderRadius: 18,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    boxShadow: "0 8px 22px rgba(106,63,214,0.4)",
    overflow: "hidden",
  },
  logoImage: {
    height: "58px",
    width: "auto",
    display: "block",
  },
  brand: {
    fontFamily: "'Sora', sans-serif",
    fontWeight: 800,
    fontSize: "22px",
    letterSpacing: "0.1px",
    backgroundImage: "linear-gradient(90deg, #6A3FD6, #B86FEA)",
    WebkitBackgroundClip: "text",
    backgroundClip: "text",
    WebkitTextFillColor: "transparent",
    color: "#2A1B3D",
  },
  tagline: { fontSize: "12.5px", color: "#A99BC7", marginTop: "3px", letterSpacing: "0.3px", fontWeight: 500 },
  datePill: {
    position: "absolute",
    right: "4px",
    top: "50%",
    transform: "translateY(-50%)",
    display: "flex",
    alignItems: "center",
    gap: "7px",
    background: "#fff",
    border: "1px solid #DCCEFF",
    color: "#6D42D8",
    fontSize: "12.5px",
    fontWeight: 700,
    padding: "8px 14px",
    borderRadius: "999px",
    boxShadow: "0 6px 20px rgba(122,80,220,.15)",
    whiteSpace: "nowrap",
  },
};
function getTodayLabel() {
  return new Date().toLocaleDateString("en-IN", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}
export default function Header() {
  return (
    <header style={styles.header} className="hvb-fade-in">
      <div style={styles.logoRow}>
        <img src={hospitalLogo} alt="Hospital logo" style={styles.logoImage} />
        <div style={styles.datePill} className="hvb-date-pill">
        <Calendar size={14} />
        <span>{getTodayLabel()}</span>
      </div>
        <div>
          <div style={styles.brand}>Ananthapuri Hospital</div>
          <div style={styles.tagline}>Care · Compassion · Commitment</div>
        </div>
      </div>
    </header>
  );
}
