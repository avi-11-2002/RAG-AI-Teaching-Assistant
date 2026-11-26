import chromadb
import re
import json

from ollama import embed, generate
from sentence_transformers import CrossEncoder
from rank_bm25 import BM250kapi

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_collection(
    name="my_collection"
)

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
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

def inference(prompt):
    stream = generate(
        model = "llama3.2",
        prompt = prompt,
        stream = True
    )

    full_response = ""
    for chunk in stream:
        content = chunk["response"]
        print(content, end="", flush=True)  
        full_response += content            
        
    print()  
    return full_response
    
incoming_query = input("Ask a question : ")
question_embedding = create_embedding([incoming_query])[0]

results = collection.query(
    query_embeddings=[question_embedding], 
    n_results=5
)

retrieved_chunks = []
for i in range(len(results["documents"][0])):
    metadata = results["metadatas"][0][1]

    retrieved_chunks.append({
        "title": metadata["title"],
        "number": metadata["number"],
        "start": metadata["start"],
        "end": metadata["end"],
        "text": results["documents"][0][i]        
    })

prompt = f'''These are the videos of WEB Development course. Here are video subtitle chunks containing video title, video number, start time in seconds, end time in seconds, the text at that time:

{retrieved_chunks}
---------------------------------
"{incoming_query}"
User asked this question related to the video chunks, you have to answer in a human way (dont mention the above format, its just for you) where and how much content is taught in which video (in which video and at what timestamp) and guide the user to go to that particular video. If user asks unrelated question, tell him that you can only answer questions related to the course
'''
with open("prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)

response = (inference(prompt))

with open("response.txt", "w", encoding="utf-8") as f:
    f.write(response)
