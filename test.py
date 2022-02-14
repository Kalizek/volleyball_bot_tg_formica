from moviepy.editor import *
import os, glob, shutil, csv

def write_csv(name):
    mas = name.split(",")
    temp = []
    print(mas)
    print(len(mas))
    if (len(mas) % 2 == 0 and len(mas) >= 2):
        return(False)
    for i in range(1,len(mas)):
        if ":" in mas[i]:
            temp = mas[i].split(":")
            mas[i] = int(temp[0]) * 60 + int(temp[1])
            print(mas[i])
    with open("DB.csv", 'a', newline = '', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=";")
                for i in range(1,len(mas)-1, 2):
                    print(i)
                    writer.writerow([mas[0],mas[i],mas[i+1]])
                return(True)

name = "GX050031.MP4" + ",6:10,6:30,10,15"
print(write_csv(name))
# def video_cut(way,start,stop,name):
#     with VideoFileClip(way) as clip:
#                 cut1 = clip.subclip(start, stop)
#                 cut1.write_videofile("Render_video/moment/" + name)