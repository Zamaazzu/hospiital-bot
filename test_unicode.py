text = "ഹൃദയം."
alias = "ഹൃദയം"

print(alias in text)
print([hex(ord(c)) for c in alias])
print([hex(ord(c)) for c in text[:len(alias)]])