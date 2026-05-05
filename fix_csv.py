import pandas as pd

with open("data/conversations.csv", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

conversation = "\\n".join([line.strip() for line in lines if line.strip() != ""])

df = pd.DataFrame({"conversation": [conversation]})
df.to_csv("data/conversations_fixed.csv", index=False)

print("✅ Fixed CSV created!")