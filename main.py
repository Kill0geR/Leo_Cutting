import os
import threading
import time
import keyboard
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx.resize import resize
import pygame
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui as pg


class TikTokCutter:
    def __init__(self):
        self.beatcounter = 0
        self.all_sekunden_pro_beat = 0
        self.finplay = False

    @staticmethod
    def berechne_bpm(song_audio):
        song_audio.write_audiofile("tmp.wav")
        driver = webdriver.Chrome()
        driver.get("https://tunebat.com/Analyzer")
        file_input = driver.find_element(by=By.CSS_SELECTOR, value="input[type='file']")
        file_input.send_keys(r"C:\Users\fawaz\Leo_Cutting\tmp.wav")
        time.sleep(2)
        while driver.find_elements(by=By.CSS_SELECTOR, value="span.RBJcL._6dq2w")[1].text == "":
            print("waiting")
            pass
        sp_key = driver.find_elements(by=By.CSS_SELECTOR, value="span.RBJcL.qlGNH")

        key = sp_key[1].text
        sp_bpm = driver.find_elements(by=By.CSS_SELECTOR, value="span.RBJcL._6dq2w")
        bpm = sp_bpm[1].text
        print("Key:", key, "/ BPM:", bpm)
        driver.quit()
        return int(bpm)

    @staticmethod
    def videos_mit_passagen_kombinieren(audio_clip, video_list, output_video, bpm, beats2drop=30, beats2cut=0):
        try:
            clips = []

            total_duration = VideoFileClip(video_list[0]).duration

            beats_pro_sekunde = bpm / 60
            frame_pro_beat = int(VideoFileClip(video_list[0]).fps / beats_pro_sekunde)
            dauer_pro_beat = (frame_pro_beat / VideoFileClip(video_list[0]).fps)
            dauer_pro_video = dauer_pro_beat * beats2cut
            print("s/beat", dauer_pro_video)
            cuts = int(total_duration // dauer_pro_video)
            print(cuts)
            video_index = 0
            for cut in range(0, cuts):
                print("cut")
                startzeit = cut * dauer_pro_video
                print(video_index)
                video = video_list[video_index]

                clip = resize(VideoFileClip(video), (1080, 1920))
                endzeit = min(startzeit + dauer_pro_video, clip.duration)
                subclip = clip.subclip(startzeit, endzeit)

                clips.append(subclip)
                video_index = video_index + 1 if video_index <= len(video_list) - 2 else 0

            audiostart = beats2drop * dauer_pro_beat

            final_clip = concatenate_videoclips(clips)
            print(final_clip.duration)
            start_audio_clip = TikTokCutter()
            final_clip = final_clip.set_audio(audio_clip.subclip(audiostart, audiostart + final_clip.duration))
            final_clip.write_videofile(output_video, codec='libx264', audio_codec='aac')
            final_clip.close()
        except OSError:
            print("Video has been created")

    def countUp(self):
        while True:
            self.beatcounter += 1
            time.sleep(self.all_sekunden_pro_beat)
            print(self.beatcounter, self.all_sekunden_pro_beat)
            if self.finplay:
                break

    @staticmethod
    def playAudio(filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

    def initialize(self):
        audio_path = 'schwarz.mp3'
        output_video = 'result.mp4'
        beats2cut = 4

        video_list = ["toCut/" + i for i in os.listdir("toCut")]
        audio_clip = AudioFileClip(audio_path)
        bpm = self.berechne_bpm(audio_clip)
        sekunden_pro_beat = 60 / bpm
        self.all_sekunden_pro_beat = sekunden_pro_beat
        print(self.beatcounter)

        self.beatcounter = 0

        audio_file = audio_path

        countUp_thread = threading.Thread(target=self.countUp)
        audio_thread = threading.Thread(target=self.playAudio, args=(audio_file,))

        countUp_thread.start()
        audio_thread.start()

        keyboard.wait("space")

        self.finplay = True

        pygame.mixer.music.stop()
        countUp_thread.join()
        print(self.beatcounter)
        self.videos_mit_passagen_kombinieren(audio_clip, video_list, output_video, bpm, self.beatcounter, beats2cut)


if __name__ == "__main__":
    init = TikTokCutter()
    init.initialize()
