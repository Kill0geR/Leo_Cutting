import threading
from playsound import playsound as ps
import playsound

def play():
    playsound(audio_path)
    play

def countUp():
    global beatcounter
    while True:
        time.sleep(sekunden_pro_beat)
        beatcounter += 1
        print(beatcounter)
        if keyboard.is_pressed("space"):
            break


is_playing = False
thread_play = threading.Thread(target=play)
thread_countUp = threading.Thread(target=countUp)

thread_play.start()
thread_countUp.start()

thread_countUp.join()
thread_play.join()

videos_mit_passagen_kombinieren(video_list, output_video, bpm, beatcounter, beats2cut)
