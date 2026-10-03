import whisper
import json 
import os

model = whisper.load_model('large-v2')

audios = os.listdir("Audios")

for audio in audios:
    title = audio.split('_')[1][:-4]
    result = model.transcribe(audio = f'Audios/{audio}',
                          language = 'hi',
                          task = 'translate',
                          word_timestamps=False)
    print(title)

    chunks = []
    for segment in result["segments"]:
        chunks.append({'title' : title, 'id' : segment["id"], "start" : segment["start"], "end" : segment["end"], "text" : segment["text"]})

    chunks_with_metadata = {"chunks": chunks, "text" : result["text"]}

    with open(f"jsons/{audio}.json", 'w') as f:
        json.dump(chunks_with_metadata, f)