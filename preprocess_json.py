import os
import json
import chromadb
from ollama import embed

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)
collection = chroma_client.get_or_create_collection(
    name="my_collection"
)

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

chunk_id = 0

for json_file in jsons:
    with open(f"newjsons/{json_file}", "r", encoding="utf-8") as f:
        content = json.load(f)
    print(f"Creating Embeddings for {json_file}")
    embeddings = create_embedding([c["text"] for c in content["chunks"]])

    for i, chunk in enumerate(content["chunks"]):
        chunk_id += 1
        collection.upsert(
            ids=[str(chunk_id)],
            embeddings = [embeddings[i]],
            documents = [chunk["text"]],
            metadatas = [{
                "title" : chunk["title"],
                "number" : chunk["number"],
                "start" : chunk["start"],
                "end" : chunk["end"]
            }]
        )
       
print("All embeddings successfully stored in ChromaDB")
print("Total chunks : ", collection.count())

