const BASE_URL = "/api";

async function handleResponse(res, label) {
  if (!res.ok) throw new Error(`${label} failed: ${res.status}`);
  return res.json();
}

export async function healthCheck() {
  const res = await fetch(`${BASE_URL}/`);
  return handleResponse(res, "Health check");
}

// GET /departments -> [{ department_id, department, dept_code }, ...]
export async function fetchDepartments() {
  const res = await fetch(`${BASE_URL}/departments`);
  return handleResponse(res, "Loading departments");
}

// GET /doctors?department_id=X
// -> { success: true, doctors: [{ schedule_id, doctor_id, doctor_name, department, tokens_left, total_tokens, report_time }] }
// -> { success: false, message } when none found
export async function fetchDoctors(departmentId) {
  const url = departmentId
    ? `${BASE_URL}/doctors?department_id=${departmentId}`
    : `${BASE_URL}/doctors`;
  const res = await fetch(url);
  const data = await handleResponse(res, "Loading doctors");
  if (data.success === false) return [];
  return data.doctors;
}

// GET /doctor/{doctor_id} -> { success, doctor: {...} }
export async function fetchDoctorDetails(doctorId) {
  const res = await fetch(`${BASE_URL}/doctor/${doctorId}`);
  const data = await handleResponse(res, "Loading doctor details");
  if (data.success === false) return null;
  return data.doctor;
}

export async function sendChatMessage(message) {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  const data = await handleResponse(res, "Chat request");
  return data.response;
}

// GET /token_status?token_number=X
// -> { success, token_number, doctor_name, department, date, status, estimated_time }
// -> { response: "Sorry, I couldn't find that token." } when not found
export async function checkTokenStatus(tokenNumber) {
  const res = await fetch(`${BASE_URL}/token_status?token_number=${encodeURIComponent(tokenNumber)}`);
  return handleResponse(res, "Token status request");
}

// POST /book
// body: { schedule_id, name, phone, age, gender }
// -> { success: true, token_number, status, doctor_name, department, hospital, date, report_time, booking_time }
// -> { success: false, message }
export async function bookToken({ scheduleId, name, age, gender, phone }) {
  const res = await fetch(`${BASE_URL}/book`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      schedule_id: scheduleId,
      name,
      age: age === "" || age === undefined ? null : Number(age),
      gender: gender || null,
      phone: phone || null,
    }),
  });
  return handleResponse(res, "Booking");
}
