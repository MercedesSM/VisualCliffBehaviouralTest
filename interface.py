import os
import tkinter as tk
from subprocess import Popen
from tkinter import *
from tkinter import filedialog
from tkinter import ttk, filedialog
from tkinter.filedialog   import askdirectory
import pygubu
import xlwt
import xlsxwriter
from datetime import datetime
import time
#import matplotlib.pyplot as plt

import getVideosFunction
from findBoxFunction import findBox
from mainApplication import application, percentPerSection

root = tk.Tk()
root.title("Visual Cliff Video Processing")
canvas = tk.Canvas(root, height=200 , width=600)
canvas.pack()

#"/Users/mercedesstringermartin/Desktop/VisualCliff/Crop"
def browse_button1():
    global folder_path1
    filename1 = filedialog.askdirectory(initialdir = "/Users/mercedesstringermartin/Desktop/VisualCliff/BL6180319/bl6_cliff/") #initialdir = '/', title ='Select folder', filetype = (("mp4", "*.mp4"),(("All Files", "*.*")
    folder_path1.set(filename1)
    print(filename1)
    entry_in.delete(0, END)
    entry_in.insert(END, filename1)

def browse_button2():
    global folder_path2
    filename2 = filedialog.askdirectory(initialdir = "/Users/mercedesstringermartin/Desktop/ExcelFiles")
    folder_path2.set(filename2)
    print(filename2)
    entry_out.delete(0, END)
    entry_out.insert(END, filename2)

frame = tk.Frame(root)
frame.place(relx = 0, rely =0, relheight = 1.5, relwidth =1)

#input
folder_path1 = StringVar()

label_in = tk.Label(frame, text="Input Directory: ")
label_in.place(relx = 0.01, rely =0.01, relheight = 0.1, relwidth =0.2)

entry_in = tk.Entry(frame)
defaulte_in = "/Users/mercedesstringermartin/Desktop/VisualCliff/Pilots/M1_one" #/Users/mercedesstringermartin/Desktop/VisualCliff/BL6180319/bl6_cliff/
entry_in.insert(END, defaulte_in)
entry_in.place(relx = 0.2, rely =0.01, relheight = 0.1, relwidth =0.65)

filename1  = entry_in.get()

browse_b1 = tk.Button(frame, text ="Browse", command = browse_button1)
browse_b1.place(relx = 0.87, rely =0.01, relheight = 0.1, relwidth =0.1)

#output

folder_path2 = StringVar()
label_out = tk.Label(frame, text="Output Directory: ")
label_out.place(relx = 0.01, rely =0.15, relheight = 0.1, relwidth =0.2)

entry_out = tk.Entry(frame)
defaulte_out = "/Users/mercedesstringermartin/Desktop/ExcelFiles"
entry_out.insert(END,defaulte_out)
entry_out.place(relx = 0.2, rely =0.15, relheight = 0.1, relwidth =0.65)

filename2 = entry_out.get()

browse_b2 = tk.Button(frame, text ="Browse", command = browse_button2)
browse_b2.place(relx = 0.87, rely =0.15, relheight = 0.1, relwidth =0.1)


# display_video

CheckVar1 = IntVar()
C1 = tk.Checkbutton(frame, text = "Display Video", variable = CheckVar1)
C1.place(relx = 0.25, rely =0.3, relheight = 0.1, relwidth =0.2) # rely =0.25


# export data

CheckVar2 = IntVar()
C2 = tk.Checkbutton(frame, text = "Export Data", variable = CheckVar2)
C2.place(relx = 0.55, rely =0.3, relheight = 0.1, relwidth =0.2)

def check2():
    if CheckVar2.get() == 1:
        export_data = True
    else:
        export_data = False
    return export_data

# Progress bar

# style = ttk.Style()
# style.configure("BW.TLabel", foreground="black", background="white")

# progressbar=ttk.Progressbar(frame,orient="horizontal",length=300, mode="determinate")
# progressbar.place(relx = 0.25, rely =0.35, relheight = 0.1, relwidth =0.5)


def start():

    videos = getVideosFunction.getVideos(filename1)


    if CheckVar1.get() == True:
        display_video = True
    else:
        display_video = False                           ### REMEMEBER TO QUIT/STOP VIDEO?

    if CheckVar2.get() == True:
        export_data = True
    else:
        export_data = False

    for countVideo, video in enumerate(videos):
        if video is None:
            print("End")
            break
        time.sleep(0.05)
        #progressbar.start()

        # progressbar["value"] = countVideo-1
        # progressbar["maximum"] = maxValue
        #
        # progressbar.update()
        #
        # divisions = len(videos)
        # for i in range(divisions):
        #     currentValue = currentValue + 1
        #     progressbar.after(i, progress(currentValue))
        #     progressbar.update()  # Force an update of the GUI

        if export_data == False:
            # corrected0xcoords, corrected0ycoords, sections, secondslist, speedlist, cornersX, cornersY = application(video,display_video)
            # plt.plot(corrected0xcoords,corrected0ycoords)
            # plt.show()
            application(video, display_video)

        if export_data == True:
            wb = xlsxwriter.Workbook('{}/Test{}.xlsx'.format(filename2,countVideo)) # Per video make a new one? Or what name should this be given? Once excel with all?
            format1 = wb.add_format({'num_format': 'dd/mm/yy'})
            sheet1 = wb.add_worksheet('Sheet 1')
            sheet1.write(0, 0,('Date:{}'.format(datetime.now(),format1)))
            sheet1.write(0, 2, 'Video number {}'.format(countVideo))
            sheet1.write(0, 3, 'Video Directory')
            sheet1.write(0, 4, '{}'.format(filename1))


            sheet1.set_column(0, 3, 15)
            sheet1.write(1, 0, 'Time (s)')
            sheet1.write(1, 1, 'X position')
            sheet1.write(1, 2, 'Y position')
            sheet1.write(1, 3, 'Speed (pxl/sec)')
            sheet1.write(1, 4, 'Section')
            sheet1.write(1, 5, 'Section Pos %')
            sheet1.write(1, 6, 'Section Speed Av')
            sheet1.write(1, 7, 'Corner X Coords')
            sheet1.write(1, 8, 'Corner Y Coords')

            corrected0xcoords, corrected0ycoords, sections, secondslist, speedlist, cornersX, cornersY  = application(video, display_video)
            percentages, averages = percentPerSection(sections, speedlist)

            # plt.plot(corrected0xcoords,corrected0ycoords)
            # plt.show()

            sheet1.write_column("A3", secondslist)
            sheet1.write_column("B3", corrected0xcoords)
            sheet1.write_column("C3", corrected0ycoords)
            sheet1.write_column("D3", speedlist)
            sheet1.write_column("E3", sections)
            sheet1.write_column("F3", percentages)
            sheet1.write_column("G3", averages)
            sheet1.write_column("H3", cornersX)
            sheet1.write_column("I3", cornersY)
            print("End")
            wb.close()

    #progressbar.stop()


start_b = tk.Button(frame, text ="Start", command = start)
start_b.place(relx = 0.25, rely =0.45, relheight = 0.1, relwidth =0.2)

# Stop
# def stop():
#
#     #stop program but doesn't close window?
#     return None
#
# stop_b = tk.Button(frame, text ="Stop", command = stop)
# stop_b.place(relx = 0.425, rely =0.5, relheight = 0.1, relwidth =0.2)

# Quit
# def quit():
#     #stops program and quits window
#     root.destroy()
#
# quit_b = tk.Button(frame, text ="Quit", command = quit)
# quit_b.place(relx = 0.65, rely =0.5, relheight = 0.1, relwidth =0.2)
def quit():
    #stops program and quits window
    root.destroy()

quit_b = tk.Button(frame, text ="Quit", command = quit)
quit_b.place(relx = 0.55, rely =0.45, relheight = 0.1, relwidth =0.2)

root.mainloop()



