from moviepy.editor import *
import os, glob, shutil


def conversion(name):
    mas = os.listdir(name)
    for i in range(len(mas)):
        video = VideoFileClip("start_video/" + str(mas[i]))
        video.write_videofile("video/" + str(mas[i]))
    for file in glob.glob("start_video/*"):
        os.remove(file)
        print("Deleted " + str(file))
    list = os.listdir("video")
    for i in range(len(list)):
        shutil.copyfile('video/' + list[i], r'C:\Users\Kalizek\YandexDisk\Video_volleyball\/' + list[i])




def video_cut(way,start,stop,name):
    with VideoFileClip(way) as clip:
                cut1 = clip.subclip(start, stop)
                cut1.write_videofile("Render_video/moment/" + name)

def gluing():
    temp = []
    mas = os.listdir("Render_video/moment")
    print(mas)
    for i in range(len(mas)):
        temp.append(VideoFileClip("Render_video/moment/" + str(mas[i])))
    final_clip = temp[0]
    for i in range(1,len(temp)):
        final_clip = concatenate_videoclips([final_clip,temp[i]])
    final_clip.write_videofile("Render_video/full/" + "full gluing" + ".mp4")