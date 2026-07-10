from backend.booking.op_schedule_lookup import lookup_available_doctors
results = lookup_available_doctors(
    department="Cardiology"
)

print(results)