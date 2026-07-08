def adapt_intent_result(user_query, extracted_result):
    """
    Converts Person 3's output into the format expected by prompts.py
    """

    slots = extracted_result.get("slots", {})

    return {
        "intent": extracted_result.get("intent"),
        "user_query": user_query,
        "department": slots.get("department"),
        "doctor": slots.get("doctor_name"),
        "date": slots.get("preferred_date"),
        "time": slots.get("preferred_time"),
        "ticket_number": slots.get("ticket_number")
    }