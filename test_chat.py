from backend.nlp.prompts import build_prompt
from backend.nlp.gemini_client import ask_gemini

intent_result={
    "intent":"general",
    "user_query":"who won ipl"
}
prompt=build_prompt(intent_result)
print("====GENERATED PROMPT=====")
print(prompt)
print("\n=====GEMINI RESPONSE=====")
reply=ask_gemini(prompt)
print(reply)