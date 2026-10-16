import subprocess 
import os 

files = os.listdir("Videos")

for file in files:
    name = file.split('com ')[1].split(' _ ')[0]
    number = file.split(' #')[1].split(' 360P.mp4')[0]
    print(number, name)
    subprocess.run(['ffmpeg', '-i', f"Videos/{file}", f"Audios/{number}_{name}.mp3"])





