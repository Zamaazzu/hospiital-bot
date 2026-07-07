def build_prompt(intent_result, database_result=None):
    """
    Routes the request to the correct prompt builder.
    """

    intent = intent_result.get("intent")

    if intent == "book_op":
        return _build_booking_prompt(intent_result, database_result)

    elif intent == "doctor_availability":
        return _build_doctor_prompt(intent_result, database_result)

    elif intent == "token_status":
        return _build_token_prompt(intent_result, database_result)

    elif intent == "hospital_info":
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
Name:{doctor.get("doctor_name","N/A")}
Department:{doctor.get("department","N/A")}
Time:{doctor.get("time","N/A")}
Tokens Left:{doctor.get("tokens_left","N/A")}"""
        for i,doctor in enumerate(database_result,start=1)
    )


#======================================
# ---------- Prompt Builders ----------
def _build_general_prompt(intent_result):
    user_query = intent_result.get("user_query", "")

    return f"""
You are an AI assistant for a Hospital OP Booking System.

Rules:
- Answer only hospital-related questions.
- Be polite and professional.
- Do not make up information.
- If the question is unrelated to hospital services, politely explain that you only assist with hospital-related queries.

User Query:
{user_query}
"""

def _build_booking_prompt(intent_result, database_result):
    rules=_common_rules()
    department=intent_result.get("department","Not specified")
    doctor=intent_result.get("doctor","Not specified")
    date=intent_result.get("date","Not specified")
    query=intent_result.get("user_query")

    doctor_details=_format_doctors(database_result)

    booking_information=f"""
    Booking Information
    User Query:
    {query}
    Requested Department
    {department}
    Requested Doctor
    {doctor}
    Requested Date
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
    pass


def _build_token_prompt(intent_result, database_result):
    pass


def _build_hospital_prompt(intent_result, database_result):
    pass


