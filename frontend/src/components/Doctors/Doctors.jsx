import React, { useEffect, useState } from "react";
import { X, ArrowLeft, ChevronRight, Clock, CheckCircle2, AlertTriangle } from "lucide-react";
import {
  DEPARTMENTS,
  DEPTS_PER_PAGE,
  TOTAL_PAGES,
  LOW_TOKEN_THRESHOLD,
  NO_SELECTION_FLOW_IDS,
} from "../../constants/departments";

const styles = {
  drawer: {
    position: "fixed",
    top: 0,
    right: 0,
    height: "100vh",
    width: "100vw",
    background: "#fff",
    zIndex: 50,
    boxShadow: "none",
    padding: "24px 20px",
    boxSizing: "border-box",
    display: "flex",
    flexDirection: "column",
    overflow: "hidden",
  },
  drawerHeader: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: "18px",
    flexShrink: 0,
    gap: "10px",
    width: "100%",
    maxWidth: "920px",
    margin: "0 auto 18px",
  },
  drawerHeaderLeft: { display: "flex", alignItems: "center", gap: "10px", minWidth: 0 },
  backBtn: {
    width: 32,
    height: 32,
    borderRadius: "16px",
    border: "1px solid #DCCEFF",
    background: "#fff",
    color: "#6D42D8",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    cursor: "pointer",
    flexShrink: 0,
    boxShadow: "0 6px 20px rgba(122,80,220,.15)",
  },
  doctorsTitle: {
    fontFamily: "'Sora', sans-serif",
    fontWeight: 700,
    fontSize: "17px",
    color: "#2A1B3D",
  },
  drawerClose: {
    width: 34,
    height: 34,
    borderRadius: "16px",
    border: "1px solid #DCCEFF",
    background: "#fff",
    color: "#6D42D8",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    cursor: "pointer",
    flexShrink: 0,
    boxShadow: "0 6px 20px rgba(122,80,220,.15)",
  },
  drawerContent: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    justifyContent: "flex-start",
    minHeight: 0,
    overflow: "auto",
    width: "100%",
    maxWidth: "920px",
    margin: "0 auto",
  },
  deptGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(150px, 1fr))",
    gap: "14px",
  },
  deptBtn: {
    position: "relative",
    border: "1px solid #DCCEFF",
    borderRadius: "16px",
    padding: "16px 12px",
    background: "#fff",
    opacity: 0,
    overflow: "hidden",
    textAlign: "left",
    cursor: "pointer",
    display: "flex",
    flexDirection: "column",
    gap: "8px",
    boxShadow: "0 6px 20px rgba(122,80,220,.15)",
  },
  deptName: { fontFamily: "'Sora', sans-serif", fontWeight: 700, fontSize: "13.5px", color: "#2A1B3D" },
  deptCount: { fontSize: "11px", color: "#9C8FBE", fontWeight: 600 },
  paginationRow: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "14px",
    marginTop: "16px",
    flexShrink: 0,
  },
  nextPageBtn: {
    display: "flex",
    alignItems: "center",
    gap: "6px",
    border: "1px solid #DCCEFF",
    background: "#fff",
    color: "#6D42D8",
    fontWeight: 700,
    fontSize: "13px",
    padding: "10px 18px",
    borderRadius: "999px",
    cursor: "pointer",
    boxShadow: "0 6px 20px rgba(122,80,220,.15)",
  },
  drawerGrid: { display: "flex", flexDirection: "column", gap: "14px" },
  drawerCardRow: { display: "flex", alignItems: "center", gap: "12px" },
  doctorCard: {
    position: "relative",
    border: "1px solid #DCCEFF",
    borderRadius: "18px",
    padding: "18px 16px",
    background: "#fff",
    opacity: 0,
    overflow: "hidden",
    boxShadow: "0 6px 20px rgba(122,80,220,.15)",
  },
  doctorCardDisabled: { background: "#F4F4F6", border: "1px solid #E1E1E6", boxShadow: "none", cursor: "not-allowed" },
  doctorName: { fontFamily: "'Sora', sans-serif", fontWeight: 700, fontSize: "14.5px", color: "#2A1B3D" },
  doctorHours: { display: "flex", alignItems: "center", fontSize: "12px", color: "#9C8FBE", marginTop: "6px" },
  generalOpText: { fontSize: "12.5px", color: "#4B3B66", lineHeight: 1.55, margin: "14px 0 12px" },
  formLabel: {
    display: "block",
    fontSize: "11.5px",
    fontWeight: 700,
    color: "#6D42D8",
    marginBottom: "6px",
    marginTop: "14px",
  },
  formInput: {
    width: "100%",
    boxSizing: "border-box",
    border: "1px solid #DCCEFF",
    borderRadius: "12px",
    padding: "10px 12px",
    fontSize: "13px",
    fontFamily: "'Inter', sans-serif",
    color: "#2A1B3D",
    background: "#FBF8FF",
    outline: "none",
  },
  formSubmitBtn: {
    width: "100%",
    marginTop: "20px",
    border: "none",
    borderRadius: "999px",
    padding: "11px 14px",
    fontSize: "13px",
    fontWeight: 700,
    color: "#fff",
    background: "linear-gradient(90deg, #8A5AE5, #6A3FD6)",
    cursor: "pointer",
    boxShadow: "0 10px 22px -8px rgba(106,63,214,0.55)",
  },
  opFormSuccess: { padding: "6px 0 4px" },
  tokenRow: { marginTop: "14px" },
  tokenTrack: { height: "5px", borderRadius: "999px", background: "#E4D6FC", overflow: "hidden", marginBottom: "8px" },
  tokenStatusRow: { display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: "6px" },
  tokenText: { fontSize: "11.5px", fontWeight: 700 },
  tokenBadge: {
    display: "inline-flex",
    alignItems: "center",
    gap: "4px",
    fontSize: "10.5px",
    fontWeight: 700,
    padding: "3px 9px",
    borderRadius: "999px",
  },
  tokenBadgeGood: { background: "#EFE7FE", color: "#6A3FD6" },
  tokenBadgeLow: { background: "#FBEAFB", color: "#8A5AE5" },
  tokenBadgeDisabled: { background: "#ECECEF", color: "#8A8A93" },
  bookingIntro: {
    fontSize: "12.5px",
    color: "#4B3B66",
    lineHeight: 1.55,
    margin: "2px 0 4px",
  },
  tokenNumberBig: {
    fontFamily: "'Sora', sans-serif",
    fontWeight: 800,
    fontSize: "22px",
    letterSpacing: "0.5px",
    color: "#6A3FD6",
    margin: "10px 0 16px",
  },
  tokenDetailRow: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "8px 0",
    borderTop: "1px solid #F1E4FD",
    fontSize: "13px",
  },
  tokenDetailLabel: { color: "#9C8FBE", fontWeight: 600 },
  tokenDetailValue: { color: "#2A1B3D", fontWeight: 700, textAlign: "right" },
  doneBtn: {
    width: "100%",
    marginTop: "18px",
    border: "1px solid #DCCEFF",
    borderRadius: "999px",
    padding: "11px 14px",
    fontSize: "13px",
    fontWeight: 700,
    color: "#6D42D8",
    background: "#fff",
    cursor: "pointer",
  },
};

function GeneralOpForm({ selectedDept, opForm, setOpForm, opFormSubmitted, setOpFormSubmitted }) {
  return (
    <div style={styles.drawerGrid}>
      <form
        className="hvb-doctor-card"
        style={{ ...styles.doctorCard, animationDelay: "0.05s" }}
        onSubmit={(e) => {
          e.preventDefault();
          setOpFormSubmitted(true);
        }}
      >
        <span className="hvb-doctor-edge" style={{ background: selectedDept.accent }} />

        {opFormSubmitted ? (
          <div style={styles.opFormSuccess}>
            <span style={{ ...styles.tokenBadge, ...styles.tokenBadgeGood }}>
              <CheckCircle2 size={12} />
              Details submitted
            </span>
            <p style={styles.generalOpText}>
              Thanks, {opForm.name || "there"}! Please proceed to the casualty counter with these
              details.
            </p>
          </div>
        ) : (
          <>
            <label style={styles.formLabel} htmlFor="op-name">
              Name
            </label>
            <input
              id="op-name"
              type="text"
              required
              placeholder="Full name"
              value={opForm.name}
              onChange={(e) => setOpForm({ ...opForm, name: e.target.value })}
              style={styles.formInput}
              className="hvb-form-input"
            />

            <label style={styles.formLabel} htmlFor="op-age">
              Age
            </label>
            <input
              id="op-age"
              type="number"
              min="0"
              max="120"
              required
              placeholder="Age"
              value={opForm.age}
              onChange={(e) => setOpForm({ ...opForm, age: e.target.value })}
              style={styles.formInput}
              className="hvb-form-input"
            />

            <label style={styles.formLabel} htmlFor="op-gender">
              Gender
            </label>
            <select
              id="op-gender"
              required
              value={opForm.gender}
              onChange={(e) => setOpForm({ ...opForm, gender: e.target.value })}
              style={styles.formInput}
              className="hvb-form-input"
            >
              <option value="" disabled>
                Select gender
              </option>
              <option value="female">Female</option>
              <option value="male">Male</option>
              <option value="other">Other</option>
            </select>

            <button type="submit" style={styles.formSubmitBtn} className="hvb-form-submit">
              Continue
            </button>
          </>
        )}
      </form>
    </div>
  );
}

function getNextTokenNumber(doctor) {
  // e.g. capacity 30, tokens (remaining) 24 → 6 already issued → next is 7
  const alreadyIssued = doctor.capacity - doctor.tokens;
  const nextNumber = alreadyIssued + 1;
  doctor.tokens = Math.max(0, doctor.tokens - 1); // one less remaining for the next person
  return nextNumber;
}

function DoctorBookingForm({ dept, doctor, form, setForm, onSubmit }) {
  return (
    <div style={styles.drawerGrid}>
      <form
        className="hvb-doctor-card"
        style={{ ...styles.doctorCard, animationDelay: "0.05s" }}
        onSubmit={onSubmit}
      >
        <span className="hvb-doctor-edge" style={{ background: dept.accent }} />

        <p style={styles.bookingIntro}>
          Booking with <strong>{doctor.name}</strong> · {doctor.hours}
        </p>

        <label style={styles.formLabel} htmlFor="booking-name">
          Name
        </label>
        <input
          id="booking-name"
          type="text"
          required
          placeholder="Full name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          style={styles.formInput}
          className="hvb-form-input"
        />

        <label style={styles.formLabel} htmlFor="booking-age">
          Age
        </label>
        <input
          id="booking-age"
          type="number"
          min="0"
          max="120"
          required
          placeholder="Age"
          value={form.age}
          onChange={(e) => setForm({ ...form, age: e.target.value })}
          style={styles.formInput}
          className="hvb-form-input"
        />
        <label style={styles.formLabel} htmlFor="booking-gender">
          Gender
        </label>
        <select
          id="booking-gender"
          required
          value={form.gender}
          onChange={(e) => setForm({ ...form, gender: e.target.value })}
          style={styles.formInput}
          className="hvb-form-input"
        >
          <option value="" disabled>
            Select gender
          </option>
          <option value="female">Female</option>
          <option value="male">Male</option>
          <option value="other">Other</option>
        </select>
        <button type="submit" style={styles.formSubmitBtn} className="hvb-form-submit">
          Get token
        </button>
      </form>
    </div>
  );
}

function TokenConfirmation({ token, accent, onDone }) {
  return (
    <div style={styles.drawerGrid}>
      <div className="hvb-doctor-card" style={{ ...styles.doctorCard, animationDelay: "0.05s" }}>
        <span className="hvb-doctor-edge" style={{ background: accent }} />

        <span style={{ ...styles.tokenBadge, ...styles.tokenBadgeGood }}>
          <CheckCircle2 size={12} />
          Token confirmed
        </span>

        <div style={styles.tokenNumberBig}>{token.tokenNumber}</div>

        <div style={styles.tokenDetailRow}>
          <span style={styles.tokenDetailLabel}>Name</span>
          <span style={styles.tokenDetailValue}>{token.name}</span>
        </div>
        <div style={styles.tokenDetailRow}>
          <span style={styles.tokenDetailLabel}>Age</span>
          <span style={styles.tokenDetailValue}>{token.age}</span>
        </div>
        <div style={styles.tokenDetailRow}>
          <span style={styles.tokenDetailLabel}>Gender</span>
          <span style={styles.tokenDetailValue}>{token.gender}</span>
        </div>
        <div style={styles.tokenDetailRow}>
          <span style={styles.tokenDetailLabel}>Department</span>
          <span style={styles.tokenDetailValue}>{token.department}</span>
        </div>
        <div style={styles.tokenDetailRow}>
          <span style={styles.tokenDetailLabel}>Doctor</span>
          <span style={styles.tokenDetailValue}>{token.doctor}</span>
        </div>

        <button type="button" onClick={onDone} style={styles.doneBtn}>
          Done
        </button>
      </div>
    </div>
  );
}

function DoctorList({ selectedDept, onSelectDoctor }) {
  return (
    <div style={styles.drawerGrid}>
      {selectedDept.doctors.map((doc, i) => {
        const pct = Math.round((doc.tokens / doc.capacity) * 100);
        const isSoldOut = doc.tokens <= 0;
        const hasTokens = !isSoldOut && doc.tokens >= LOW_TOKEN_THRESHOLD;
        return (
          <div
            key={doc.name}
            className={`hvb-doctor-card ${isSoldOut ? "hvb-doctor-card-disabled" : ""}`}
            style={{
              ...styles.doctorCard,
              ...(isSoldOut ? styles.doctorCardDisabled : null),
              animationDelay: `${0.08 * i + 0.05}s`,
            }}
            role="button"
            tabIndex={isSoldOut ? -1 : 0}
            aria-disabled={isSoldOut}
            onClick={(e) => {
              if (isSoldOut) {
                e.preventDefault();
                e.stopPropagation();
                return;
              }
              onSelectDoctor(doc);
            }}
          >
            <span className="hvb-doctor-edge" style={{ background: isSoldOut ? "#C9C9D1" : selectedDept.accent }} />
            <div style={styles.drawerCardRow}>
              <div
                className="hvb-doctor-icon"
                style={
                  isSoldOut
                    ? { background: "#ECECEF", color: "#9A9AA3" }
                    : { background: selectedDept.tint, color: selectedDept.accent }
                }
              >
                <selectedDept.Icon size={22} />
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ ...styles.doctorName, ...(isSoldOut ? { color: "#9A9AA3" } : null) }}>
                  {doc.name}
                </div>
                <div style={styles.doctorHours}>
                  <Clock size={13} style={{ marginRight: 6, flexShrink: 0 }} />
                  {doc.hours}
                </div>
              </div>
            </div>

            <div style={styles.tokenRow}>
              <div style={styles.tokenTrack}>
                <div
                  className="hvb-token-fill"
                  style={{ width: `${Math.max(pct, 0)}%`, background: isSoldOut ? "#C9C9D1" : selectedDept.accent }}
                />
              </div>
              <div style={styles.tokenStatusRow}>
                <span style={{ ...styles.tokenText, color: isSoldOut ? "#9A9AA3" : selectedDept.accent }}>
                  {isSoldOut ? "No tokens left" : `${doc.tokens} tokens left`}
                </span>
                <span
                  style={{
                    ...styles.tokenBadge,
                    ...(isSoldOut ? styles.tokenBadgeDisabled : hasTokens ? styles.tokenBadgeGood : styles.tokenBadgeLow),
                  }}
                >
                  {isSoldOut ? <X size={12} /> : hasTokens ? <CheckCircle2 size={12} /> : <AlertTriangle size={12} />}
                  {isSoldOut ? "Fully booked" : hasTokens ? "Available" : "Low tokens"}
                </span>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

/**
 * The doctors/departments drawer. Handles two flows:
 *  - default: department grid (paged) → doctor list for that department
 *  - General OP: skips department selection, shows a name/age/gender form
 */
export default function Doctors({
  show,
  selectedDept,
  setSelectedDept,
  deptPage,
  setDeptPage,
  onClose,
  opForm,
  setOpForm,
  opFormSubmitted,
  setOpFormSubmitted,
}) {
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [bookingForm, setBookingForm] = useState({ name: "", age: "", gender: "" });
  const [bookedToken, setBookedToken] = useState(null);

  // Reset the doctor-booking flow whenever the department changes (including
  // going back to the department grid) or the drawer closes, so a stale
  // token/form doesn't linger the next time it's opened.
  useEffect(() => {
    setSelectedDoctor(null);
    setBookingForm({ name: "", age: "", gender: "" });
    setBookedToken(null);
  }, [selectedDept]);

  useEffect(() => {
    if (!show) {
      setSelectedDoctor(null);
      setBookingForm({ name: "", age: "", gender: "" });
      setBookedToken(null);
    }
  }, [show]);

  useEffect(() => {
    if (!show) return;
    const onKey = (e) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [show, onClose]);

  const pageDepartments = DEPARTMENTS.slice(
    deptPage * DEPTS_PER_PAGE,
    deptPage * DEPTS_PER_PAGE + DEPTS_PER_PAGE
  );

  const handleBack = () => {
    if (bookedToken || selectedDoctor) {
      setSelectedDoctor(null);
      setBookingForm({ name: "", age: "", gender: "" });
      setBookedToken(null);
      return;
    }
    setSelectedDept(null);
  };

  const handleBookingSubmit = (e) => {
    e.preventDefault();
    setBookedToken({
     tokenNumber: getNextTokenNumber(selectedDoctor),
      name: bookingForm.name,
      age: bookingForm.age,
      gender: bookingForm.gender,
      department: selectedDept.name,
      doctor: selectedDoctor.name,
    });
  };

  const drawerTitle = bookedToken
    ? "Your token"
    : selectedDoctor
    ? selectedDoctor.name
    : selectedDept
    ? selectedDept.name
    : "Choose a department";

  return (
    <>
      <div className={`hvb-backdrop ${show ? "hvb-backdrop-open" : ""}`} onClick={onClose} />

      <aside
        role="dialog"
        aria-label="Today's available doctors"
        style={styles.drawer}
        className={`hvb-drawer ${show ? "hvb-drawer-open" : ""}`}
      >
        <div style={styles.drawerHeader}>
          <div style={styles.drawerHeaderLeft}>
            {selectedDept && !NO_SELECTION_FLOW_IDS.includes(selectedDept.id) && (
              <button
                onClick={handleBack}
                style={styles.backBtn}
                className="hvb-back-btn"
                aria-label="Back"
              >
                <ArrowLeft size={17} />
              </button>
            )}
            <div style={styles.doctorsTitle}>{drawerTitle}</div>
          </div>
          <button onClick={onClose} style={styles.drawerClose} className="hvb-drawer-close" aria-label="Close">
            <X size={18} />
          </button>
        </div>

        <div style={styles.drawerContent}>
          {!selectedDept && (
            <>
              <div style={styles.deptGrid}>
                {pageDepartments.map((dept, i) => (
                  <button
                    key={dept.id}
                    onClick={() => setSelectedDept(dept)}
                    className="hvb-dept-btn"
                    style={{
                      ...styles.deptBtn,
                      animationPlayState: show ? "running" : "paused",
                      animationDelay: `${0.07 * i + 0.1}s`,
                    }}
                  >
                    <span className="hvb-doctor-edge" style={{ background: dept.accent }} />
                    <div className="hvb-doctor-icon" style={{ background: dept.tint, color: dept.accent }}>
                      <dept.Icon size={22} />
                    </div>
                    <div style={styles.deptName}>{dept.name}</div>
                    <div style={styles.deptCount}>
                      {dept.doctors.length} doctor{dept.doctors.length > 1 ? "s" : ""}
                    </div>
                  </button>
                ))}
              </div>

              {deptPage < TOTAL_PAGES - 1 && (
                <div style={styles.paginationRow}>
                  <button
                    onClick={() => setDeptPage((p) => Math.min(p + 1, TOTAL_PAGES - 1))}
                    className="hvb-next-page-btn"
                    style={styles.nextPageBtn}
                  >
                    Next page
                    <ChevronRight size={16} />
                  </button>
                </div>
              )}
            </>
          )}

          {selectedDept && selectedDept.id === "general-op" && (
            <GeneralOpForm
              selectedDept={selectedDept}
              opForm={opForm}
              setOpForm={setOpForm}
              opFormSubmitted={opFormSubmitted}
              setOpFormSubmitted={setOpFormSubmitted}
            />
          )}

          {selectedDept &&
            !NO_SELECTION_FLOW_IDS.includes(selectedDept.id) &&
            !selectedDoctor && <DoctorList selectedDept={selectedDept} onSelectDoctor={setSelectedDoctor} />}

          {selectedDept && selectedDoctor && !bookedToken && (
            <DoctorBookingForm
              dept={selectedDept}
              doctor={selectedDoctor}
              form={bookingForm}
              setForm={setBookingForm}
              onSubmit={handleBookingSubmit}
            />
          )}

          {bookedToken && (
            <TokenConfirmation token={bookedToken} accent={selectedDept.accent} onDone={onClose} />
          )}
        </div>
      </aside>
    </>
  );
}
