from moviepy.editor import *
import os, glob, shutil, csv

def read_csv():
    mas = []
    with open('DB.csv', 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            mas.append(row)
        return(mas)

def sortic(read_mas):
    read_mas.sort()
    print(read_mas)
    temp = []
    for w in range(len(read_mas)):
        for h in range(w+1,len(read_mas)):
            print(w,h)
            if read_mas[w][0] == read_mas[h][0]:
                if int(read_mas[h][1]) - 10  < int(read_mas[w][1]) < int(read_mas[h][1]) + 10:
                    if read_mas[h][1] < read_mas[w][1]:
                        read_mas[w][0] = 0
                    else:
                        read_mas[h][0] = 0
    return(read_mas)

def render():
    read_mas = read_csv()
    read_mas = sortic(read_mas)
    print(read_mas)
    for i in range(len(read_mas)):
        if read_mas[i][0] != 0:
            video_cut(r"C:\Users\Kalizek\YandexDisk\Video_volleyball\\" + read_mas[i][0], read_mas[i][1], read_mas[i][2], str(i) + ".mp4")
    os.remove("DB.csv")

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