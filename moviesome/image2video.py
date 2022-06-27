from moviepy.editor import ImageSequenceClip, VideoFileClip, AudioFileClip, afx, CompositeAudioClip
import requests
import os
import cv2

def save_image():
    url = "http://127.0.0.1:8000/test"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
    }
    res = requests.get(url).json()
    for index, one in enumerate(res["data"]):
        response = requests.get(one, headers=headers)
        image = response.content
        with open(f'./image/{index}.jpg', 'wb') as f:
            f.write(image)


def str2int(v_str: str):
    return int(v_str.replace(".png", ""))


def resize_image_keep_ratio(file_in: str, file_out: str, target_size: tuple):
    """
    在不变形的前提下，对图片进行更改尺寸
    """
    img = cv2.imread(file_in)
    old_size = img.shape[:2]
    ratio = min(float(target_size[i]) / (old_size[i]) for i in range(len(old_size)))
    new_size = tuple([int(i * ratio) for i in old_size])
    img = cv2.resize(img, (new_size[1], new_size[0]))
    pad_w = target_size[1] - new_size[1]
    pad_h = target_size[0] - new_size[0]
    top, bottom = pad_h // 2, pad_h - (pad_h // 2)
    left, right = pad_w // 2, pad_w - (pad_w // 2)
    img_new = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, None, (255, 255, 255))
    cv2.imwrite(file_out, img_new)


def create_video_from_images():
    # 拿到所有图片
    image_paths = [x for x in os.listdir("./image") if x.endswith("jpg")]
    # 删除
    [os.remove(f"./image/{x}") for x in os.listdir("./image") if x.endswith("png")]
    # 图片大小进行统一
    [resize_image_keep_ratio(file_in=f"./image/{x}",
                  file_out=f"./image/{x}".replace(".jpg", ".png"),
                  target_size=(2000, 1200)) for x in image_paths]
    # 拿到所有统一过后的图片
    image_paths = [x for x in os.listdir("./image") if x.endswith("png")]
    # 对图片进行排序
    image_paths_dic = dict(zip(image_paths, [str2int(x) for x in image_paths]))
    image_paths_sort = sorted(image_paths_dic.items(), key=lambda x: x[1])
    image_paths = [x[0] for x in image_paths_sort]
    image_paths = [f"./image/{x}" for x in image_paths]

    res_image_paths = []
    for one in image_paths:
        res_image_paths.extend([one for _ in range(50)])

    print(res_image_paths)

    clip = ImageSequenceClip(res_image_paths, fps=25)
    clip.write_videofile("done4.mp4")

    # 新生成的视频
    video_clip = VideoFileClip("done4.mp4")
    # 背景音乐
    audio_clip = AudioFileClip("reai105.mp3")
    # 设置背景音乐循环，时间与视频时间一致
    audio = afx.audio_loop(audio_clip, duration=video_clip.duration)
    # # 视频声音与背景音乐音频叠加
    # audio_clip_add = CompositeAudioClip([video_clip, audio])
    # 视频写入背景声音
    final_video = video_clip.set_audio(audio)
    # 将处理完成的视频保存
    final_video.write_videofile("video_result.mp4")


if __name__ == '__main__':
    create_video_from_images()
