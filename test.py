from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips


def videos_mit_passagen_kombinieren(video_list, audio_path, dauer_pro_video, output_video):
    clips = []

    total_duration = VideoFileClip(video_list[0]).duration

    audio_clip = AudioFileClip(audio_path)

    for startzeit in range(0, int(total_duration), dauer_pro_video):
        video_index = startzeit // dauer_pro_video % len(video_list)
        video = video_list[video_index]

        clip = VideoFileClip(video)

        endzeit = min(startzeit + dauer_pro_video, clip.duration)
        subclip = clip.subclip(startzeit, endzeit)

        subclip = subclip.set_audio(audio_clip.subclip(startzeit, endzeit))

        clips.append(subclip)

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_video, codec='libx264', audio_codec='aac')
    final_clip.close()


video_list = ['toCut/IMG_1790.mov', 'toCut/IMG_1794.mov']
audio_path = 'trim_schwarz.mp3'
dauer_pro_video = 3
output_video = 'leo_cutting.mp4'

videos_mit_passagen_kombinieren(video_list, audio_path, dauer_pro_video, output_video)
