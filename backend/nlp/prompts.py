def build_prompt(intent_result, database_result=None):
    """
    Routes the request to the correct prompt builder.
    """

    intent = intent_result.get("intent")

    if intent == "token_booking":
        return _build_booking_prompt(intent_result, database_result)

    elif intent == "doctor_availability":
        return _build_doctor_prompt(intent_result, database_result)

    elif intent == "token_status":
        return _build_token_prompt(intent_result, database_result)

    elif intent == "op_enquiry":
        return _build_hospital_prompt(intent_result, database_result)

    else:
        return _build_general_prompt(intent_result)
    


#=====================================  
# ---------- Shared Helpers ----------
def _common_rules():
    """
    Returns the common instructions shared by all prompts.
    """

    return """
You are an AI assistant for a Hospital OP Booking System.

Rules:
- Answer only hospital-related questions.
- Be polite and professional.
- Use ONLY the information provided in the prompt.
- Do NOT invent doctors, departments, timings, or token numbers.
- If required information is missing, politely ask the user for it.
- Do NOT confirm a booking unless the backend explicitly states that it has been booked.
- If the user's question is unrelated to hospital services, politely explain that you only assist with hospital-related queries.
"""

def _format_doctors(database_result):
    """
    Formats doctor records into readable string for gemini
    """
    if not database_result:
        return "No Doctors are available"
    return "\n\n".join(
        f"""Doctor {i}
-------
Doctor:{doctor.get("doctor_name","N/A")}
Department:{doctor.get("department","N/A")}
Time:{doctor.get("time","N/A")}
Tokens Left:{doctor.get("tokens_left","N/A")}"""
        for i,doctor in enumerate(database_result,start=1)
    )

def _format_token(database_result):
    """
    Formats token information into a readable string for Gemini.
    """

    if not database_result:
        return "No token information is available."

    return f"""
Token Information

Token Number: {database_result.get("token_number", "N/A")}
Doctor: {database_result.get("doctor_name", "N/A")}
Department: {database_result.get("department", "N/A")}
Date: {database_result.get("date", "N/A")}
Status: {database_result.get("status", "N/A")}
Estimated Time: {database_result.get("estimated_time", "N/A")}
"""

def _format_hospital(database_result):
    """
    Formats hospital information into a readable string for Gemini.
    """
    if not database_result:
        return "No hospital information is available."
    departments=database_result.get("departments",[])
    if departments:
        department_list = "\n".join(f"- {dept}" for dept in departments)
    else:
        department_list = "N/A"

    return f"""
Hospital Information

Hospital Name: {database_result.get("hospital_name", "N/A")}
Address: {database_result.get("address", "N/A")}
Contact: {database_result.get("contact", "N/A")}
Departments:{department_list}
"""


#======================================
# ---------- Prompt Builders ----------
def _build_general_prompt(intent_result):
    rules=_common_rules()
    query = intent_result.get("user_query")

    return f"""
    {rules}
    User Query:
    {query}
Generate a short, polite and professional response.

Answer only the user's question.

If the question is unrelated to hospital services,
politely explain that you only assist with hospital-related queries.
"""

def _build_booking_prompt(intent_result, database_result):
    rules=_common_rules()
    department=intent_result.get("department","Not specified")
    doctor=intent_result.get("doctor","Not specified")
    date=intent_result.get("date","Not specified")
    query=intent_result.get("user_query","")

    doctor_details=_format_doctors(database_result)

    booking_information=f"""
    Booking Information
    User Query:
    {query}
    Requested Department:
    {department}
    Requested Doctor:
    {doctor}
    Requested Date:
    {date}
    """

    database_information=f"""
    Available Doctors
    {doctor_details}
    """

    return f"""
    {rules}
    {booking_information}
    {database_information}

Generate a short, polite and professional response.

Do not invent information.

If multiple doctors are available,
present them as options.

If only one doctor is available,
ask the user whether they would like
to continue with the booking."""


def _build_doctor_prompt(intent_result, database_result):
    rules=_common_rules()
    department=intent_result.get("department","Not specified")
    doctor=intent_result.get("doctor","Not specified")
    date=intent_result.get("date","Not specified")
    query=intent_result.get("user_query","")

    doctor_details=_format_doctors(database_result)

    doctor_information=f"""
    Doctor Availability Request
    User Query:
    {query}
    Requested Department:
    {department}
    Requested Doctor:
    {doctor}
    Requested Date:
    {date}
    """

    database_information=f"""
    Available Doctors
    {doctor_details}
    """

    return f"""
    {rules}
    {doctor_information}
    {database_information}

Generate a short, polite and professional response.

Use only the doctor information provided.

If multiple doctors are available,
list them clearly.

If only one doctor is available,
inform the user.

Do not assume the user wants to book an appointment 
unless they explicitly ask to do so."""


def _build_token_prompt(intent_result, database_result):
    rules=_common_rules()
    query=intent_result.get("user_query","")
    token_information=_format_token(database_result)
    return f"""
    {rules}
    User Query:
    {query}
    {token_information}
Generate a short, polite and professional response.

Use only the token information provided.

Do not invent token numbers, statuses or estimated waiting times.

If token information is unavailable,
politely inform the user."""


def _build_hospital_prompt(intent_result, database_result):
    rules=_common_rules()
    query=intent_result.get("user_query","")
    hospital_information=_format_hospital(database_result)
    return f"""
    {rules}
    User query:
    {query}
    {hospital_information}

Generate a short, polite and professional response.

Use only the hospital information provided.

Do not invent hospital facilities, departments, contact information, or services.

If the requested information is unavailable,
politely inform the user.
"""


