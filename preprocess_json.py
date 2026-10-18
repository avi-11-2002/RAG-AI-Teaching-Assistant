import os
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from ollama import embed

def create_embedding(text_list):
    batch_size = 32
    all_embeddings = []
    for i in range(0, len(text_list), batch_size):
        batch = text_list[i : i + batch_size]
        response = embed(
            model="bge-m3",
            input=batch
    )
        all_embeddings.extend(response["embeddings"])
    return all_embeddings

jsons = sorted(os.listdir("newjsons"))
my_dicts = []
chunk_id = 0

for json_file in jsons:
    with open(f"newjsons/{json_file}", "r", encoding="utf-8") as f:
        content = json.load(f)
    print(f"Creating Embeddings for {json_file}")
    embeddings = create_embedding([c["text"] for c in content["chunks"]])

    for i, chunk in enumerate(content["chunks"]):
        chunk["chunk_id"] = chunk_id
        chunk["embedding"] = embeddings[i]
        chunk_id += 1
        my_dicts.append(chunk)
        
df = pd.DataFrame.from_records(my_dicts)
joblib.dump(df, "embeddings.joblib")

