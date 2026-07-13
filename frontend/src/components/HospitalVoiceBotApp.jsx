import React, { useState, useCallback } from "react";
import Header from "./Header/Header";
import Hero from "./Hero/Hero";
import Doctors from "./Doctors/Doctors";
import Footer from "./Footer/Footer";
import { GENERAL_OP } from "../constants/departments";
import { styleForDeptName } from "./Doctors/Doctors";
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
  const [isListening, setIsListening] = useState(false);
  const [showDoctors, setShowDoctors] = useState(false);
  const [deptPage, setDeptPage] = useState(0);
  const [selectedDept, setSelectedDept] = useState(null);
  const [opForm, setOpForm] = useState({ name: "", age: "", gender: "" });
  const [opFormSubmitted, setOpFormSubmitted] = useState(false);
  const [botReply, setBotReply] = useState(null);

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

  // The bot's spoken/text reply comes up from VoiceBot (via the /voice
  // endpoint) and gets shown in the conversation bubble — see Hero.jsx and
  // Conversation.jsx's `message` prop. When the backend also resolved a
  // department from what was said (e.g. "cardiology"), open that
  // department's page directly instead of leaving the person to find it
  // themselves in the grid.
  const handleReply = useCallback((replyText, departmentMatch) => {
    setBotReply(replyText || null);

    if (departmentMatch?.id) {
      setSelectedDept({
        id: departmentMatch.id,
        name: departmentMatch.name,
        ...styleForDeptName(departmentMatch.name),
      });
      setDeptPage(0);
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
          botReply={botReply}
          onReply={handleReply}
          showDoctors={showDoctors}
          onOpenDoctors={openDoctors}
          onOpenGeneralOp={openGeneralOp}
        />

        <Footer />
      </div>
    </div>
  );
}
