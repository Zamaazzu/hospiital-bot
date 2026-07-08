import React, { useState, useCallback } from "react";
import Header from "./Header/Header";
import Hero from "./Hero/Hero";
import Doctors from "./Doctors/Doctors";
import Footer from "./Footer/Footer";
import { DEPARTMENTS, GENERAL_OP } from "../constants/departments";
import { matchDepartment } from "../utils/matchDepartment";
import "../styles/voicebot.css";

const styles = {
  canvas: {
    position: "relative",
    fontFamily: "'Inter', sans-serif",
    background: "#F8F4FE",
    height: "100vh",
    width: "100%",
    color: "#2A1B3D",
    boxSizing: "border-box",
    overflow: "hidden",
  },
  page: {
    position: "relative",
    zIndex: 1,
    width: "100%",
    maxWidth: "100%",
    height: "100%",
    margin: "0",
    padding: "18px 20px 16px",
    display: "flex",
    flexDirection: "column",
    gap: "0px",
    boxSizing: "border-box",
  },
};

export default function HospitalVoiceBotApp() {
  const [isListening, setIsListening] = useState(true);
  const [showDoctors, setShowDoctors] = useState(false);
  const [deptPage, setDeptPage] = useState(0);
  const [selectedDept, setSelectedDept] = useState(null);
  const [opForm, setOpForm] = useState({ name: "", age: "", gender: "" });
  const [opFormSubmitted, setOpFormSubmitted] = useState(false);

  const openDoctors = () => {
    setSelectedDept(null);
    setDeptPage(0);
    setShowDoctors(true);
  };

  const openGeneralOp = () => {
    setOpForm({ name: "", age: "", gender: "" });
    setOpFormSubmitted(false);
    setSelectedDept(GENERAL_OP);
    setShowDoctors(true);
  };

  const closeDoctors = () => setShowDoctors(false);

  // Voice-driven navigation: open a department (or General OP) when the
  // user says its name. VoiceBot doesn't know about departments — it just
  // reports the transcript here, and this is where that gets interpreted.
  const handleTranscript = useCallback((transcript) => {
    if (!transcript) return;
    const lower = transcript.toLowerCase();

    if (lower.includes("general") || lower.includes("casualty")) {
      setOpForm({ name: "", age: "", gender: "" });
      setOpFormSubmitted(false);
      setSelectedDept(GENERAL_OP);
      setShowDoctors(true);
      return;
    }

    const match = matchDepartment(lower, DEPARTMENTS);
    if (match) {
      setSelectedDept(match);
      setShowDoctors(true);
    }
  }, []);

  return (
    <div style={styles.canvas}>
      <div className="hvb-mesh" />

      <Doctors
        show={showDoctors}
        selectedDept={selectedDept}
        setSelectedDept={setSelectedDept}
        deptPage={deptPage}
        setDeptPage={setDeptPage}
        onClose={closeDoctors}
        opForm={opForm}
        setOpForm={setOpForm}
        opFormSubmitted={opFormSubmitted}
        setOpFormSubmitted={setOpFormSubmitted}
      />

      <div style={styles.page}>
        <Header />

        <Hero
          isListening={isListening}
          onToggleListening={() => setIsListening((v) => !v)}
          onTranscript={handleTranscript}
          showDoctors={showDoctors}
          onOpenDoctors={openDoctors}
          onOpenGeneralOp={openGeneralOp}
        />

        <Footer />
      </div>
    </div>
  );
}
