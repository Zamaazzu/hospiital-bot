from backend.nlp.intent_extractor import load_gazetteer, alias_map
import backend.nlp.intent_extractor as ie

load_gazetteer()

text = "ഹൃദയം."
text_lower = text.lower()

print(f"Total aliases loaded: {len(ie.alias_map)}")
print(f"Is 'ഹൃദയം' a key in alias_map? {'ഹൃദയം' in ie.alias_map}")

for alias, official in ie.alias_map.items():
    if "ഹൃദയം" in alias or alias in "ഹൃദയം":
        print(f"Found related alias: {repr(alias)} -> {official}")