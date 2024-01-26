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
    def __init__(self, audio_path, output_filename, videodir="/toCut", beats2cut=4):
        self.audio_path = audio_path
        self.output_video = output_filename
        self.beats2cut = beats2cut
        self.videodir = videodir
        self.final_clip = "Not Set"
        self.beatcounter = "Not Set"
        self.bpm = "Not Set"
        self.spb = "Not Set"
        self.finplay = False
        self.video_list = [self.videodir + i for i in os.listdir(self.videodir)]
        self.audio_clip = AudioFileClip(self.audio_path)

    def set_bpm(self, song_audio):
        song_audio.write_audiofile("tmp.wav")
        driver = webdriver.Chrome()
        driver.get("https://tunebat.com/Analyzer")
        file_input = driver.find_element(by=By.CSS_SELECTOR, value="input[type='file']")
        file_input.send_keys(os.path.abspath(os.getcwd()) + r"\tmp.wav")
        accept = pg.locateCenterOnScreen("accept.png")
        pg.click(accept)
        while driver.find_elements(by=By.CSS_SELECTOR, value="span.RBJcL._6dq2w")[1].text == "":
            print("waiting")
            pass

        sp_bpm = driver.find_elements(by=By.CSS_SELECTOR, value="span.RBJcL._6dq2w")
        bpm = sp_bpm[1].text
        print("BPM:", bpm)
        driver.quit()
        self.spb = 60 / int(bpm)
        self.bpm = int(bpm)

    def cut_videos(self, audio_clip, beats2drop=32):
        if self.bpm != "Not Set":
            try:
                clips = []

                total_duration = VideoFileClip(self.video_list[0]).duration

                beats_pro_sekunde = self.bpm / 60
                frame_pro_beat = int(VideoFileClip(self.video_list[0]).fps / beats_pro_sekunde)
                dauer_pro_beat = (frame_pro_beat / VideoFileClip(self.video_list[0]).fps)
                dauer_pro_video = dauer_pro_beat * self.beats2cut
                print("s/beat", dauer_pro_video)
                cuts = int(total_duration // dauer_pro_video)
                print(cuts)
                video_index = 0
                for cut in range(0, cuts):
                    print("cut")
                    startzeit = cut * dauer_pro_video
                    print(video_index, self.video_list)
                    video = self.video_list[video_index]

                    clip = resize(VideoFileClip(video), (1080, 1920))
                    endzeit = min(startzeit + dauer_pro_video, clip.duration)
                    subclip = clip.subclip(startzeit, endzeit)

                    clips.append(subclip)
                    video_index = video_index + 1 if video_index <= len(self.video_list) - 2 else 0

                print(beats2drop, self.spb)
                audiostart = beats2drop * self.spb

                final_clip = concatenate_videoclips(clips)
                print(final_clip.duration)
                self.final_clip = final_clip.set_audio(audio_clip.subclip(audiostart, audiostart + final_clip.duration))
            except OSError:
                print("Video has been created, but an OSError occured. This should not be fatal.")
        else:
            print("BPM not set yet!")

    def write(self):
        if self.final_clip != "Not Set":
            self.final_clip.write_videofile(self.output_video, codec='libx264', audio_codec='aac')
            self.final_clip.close()
        else:
            print("Video not Cut yet!")

    def countup(self):
        while True:
            self.beatcounter += 1
            time.sleep(self.spb)
            print(self.beatcounter)
            if self.finplay:
                break

    @staticmethod
    def playaudio(filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

    def cut_no_gui(self):
        self.set_bpm(self.audio_clip)
        self.beatcounter = 0
        countup_thread = threading.Thread(target=self.countup)
        audio_thread = threading.Thread(target=self.playaudio, args=(self.audio_path,))
        countup_thread.start()
        audio_thread.start()
        keyboard.wait("space")
        self.finplay = True
        pygame.mixer.music.stop()
        countup_thread.join()
        print(self.beatcounter)
        self.cut_videos(self.audio_clip)


if __name__ == "__main__":
    _audio_path = "schwarz.mp3"
    _output_filename = "result.mp4"
    _videodir = "toCut/"
    _beats2cut = 4
    cutter = TikTokCutter(_audio_path, _output_filename, _videodir, _beats2cut)
    cutter.cut_no_gui()
