from backend.nlp.gemini_client import ask_gemini

print("Testing Gemini connection...")

reply = ask_gemini("Say hello in one short sentence.")

print("\nGemini replied:")
print(reply)