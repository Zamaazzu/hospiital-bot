import React from "react";
import { Heart } from "lucide-react";

const styles = {
  footer: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "8px",
    textAlign: "center",
    background: "linear-gradient(90deg, #2C1454, #6A3FD6)",
    color: "#E7DBFC",
    fontSize: "12px",
    fontWeight: 500,
    padding: "14px",
    borderRadius: "16px",
    flexShrink: 0,
  },
};

export default function Footer() {
  return (
    <footer style={styles.footer} className="hvb-fade-in hvb-delay-2">
      <span>© 2026 Ananthapuri Hospital. All rights reserved.</span>
      <Heart size={13} className="hvb-heart" fill="#E7DBFC" color="#E7DBFC" />
    </footer>
  );
}
