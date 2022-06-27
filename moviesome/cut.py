from moviepy.editor import VideoFileClip, concatenate_videoclips

FILE_PATH = "/Users/tangzhenyuan/Desktop/downloadS/beec542604a9d025b032b6f5acd3b388.mp4"

video1 = VideoFileClip(FILE_PATH).subclip(10, 20)

video2 = VideoFileClip(FILE_PATH).subclip(40, 50)

video3 = VideoFileClip(FILE_PATH).subclip(400, 410)

# myclip.write_videofile("done1.mp4", audio_codec="aac")
final_clip = concatenate_videoclips([video1, video2, video3], method="compose")
final_clip.write_videofile("done1.mp4", audio_codec="aac")
