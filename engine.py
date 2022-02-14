import csv, os
from Video_redactor import video_cut

def write_csv_Offer(name):
    temp = []
    temp.append(name)
    with open("Offer.csv", 'a', newline = '', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=";")
                    writer.writerow([temp[0]])

def write_csv(name):
    mas = name.split(",")
    temp = []
    print(mas)
    print(len(mas))
    try:
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
    except:
        return(False)

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