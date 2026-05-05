import pandas as pd
import pickle

from rag.topic_detection import detect_topics
from rag.summarizer import summarize
from rag.retriever import VectorStore
from persona.persona_builder import build_persona

print("STARTING...")

# Load CSV
df = pd.read_csv("data/conversations_fixed.csv", encoding="utf-8")

messages = []
col = df.columns[0]

for row in df[col]:
    if isinstance(row, str):
        messages.extend(row.split("\\n"))

print("Total messages:", len(messages))

# Topics
topics = detect_topics(messages)

print("\nTopics detected:")
for i, t in enumerate(topics):
    print(f"Topic {i+1}: {t['start']} to {t['end']}")

# Topic summaries
topic_summaries = []
for t in topics:
    topic_summaries.append(summarize(t["messages"]))

print("\nTopic summaries:")
for s in topic_summaries:
    print(s)

# 100 message summaries
chunk_summaries = []
for i in range(0, len(messages), 100):
    chunk_summaries.append(summarize(messages[i:i+100]))

# Store
store = VectorStore()
store.add(topic_summaries + chunk_summaries + messages)

# Persona
persona = build_persona(messages)

print("\nPersona:")
print(persona)

# Save
with open("store.pkl", "wb") as f:
    pickle.dump(store, f)

with open("persona.pkl", "wb") as f:
    pickle.dump(persona, f)

print("\n✅ DONE")