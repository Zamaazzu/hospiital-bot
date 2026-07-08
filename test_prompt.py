from backend.nlp.prompts import build_prompt

intent_result={
    "intent":"general",
    "user_query":"Hello"
}
prompt=build_prompt(intent_result)
print(prompt)
