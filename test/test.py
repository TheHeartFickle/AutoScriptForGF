import json

D = {"a": None}
F = {}
with open("test.json", "r", encoding='utf-8') as f:
    # json.dump(D, f)
    F = json.load(f)

print(F)

