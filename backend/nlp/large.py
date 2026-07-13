from backend.nlp.intent_extractor import load_model, extract_department

load_model()

text = "കാർഡിയോളജി വിഭാഗത്തിൽ ടോക്കൺ വേണം."

print("Department:", extract_department(text))