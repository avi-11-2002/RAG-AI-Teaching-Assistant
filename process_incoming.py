import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from ollama import embed, generate

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
    

df = joblib.load("embeddings.joblib")

incoming_query = input("Ask a question : ")
question_embedding = create_embedding([incoming_query])[0]

similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()

top_result = 5
max_index = similarities.argsort()[::-1][0:top_result]

new_df = df.loc[max_index]

prompt = f'''I am teaching web development in my Sigma web development course. Here are video subtitle chunks containing video title, video number, start time in seconds, end time in seconds, the text at that time:

{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}
---------------------------------
"{incoming_query}"
User asked this question related to the video chunks, you have to answer in a human way (dont mention the above format, its just for you) where and how much content is taught in which video (in which video and at what timestamp) and guide the user to go to that particular video. If user asks unrelated question, tell him that you can only answer questions related to the course
'''
with open("prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)

response = (inference(prompt))

with open("response.txt", "w", encoding="utf-8") as f:
    f.write(response)
