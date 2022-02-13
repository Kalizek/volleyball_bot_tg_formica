import shutil,os

list = os.listdir("video")
for i in range(len(list)):
    shutil.copyfile('video/' + list[i], r'C:\Users\Kalizek\YandexDisk\Video_ volleyball\/' + list[i])
