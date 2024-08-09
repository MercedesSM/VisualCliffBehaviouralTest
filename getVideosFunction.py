import cv2 as cv
import numpy as np
import os.path
from connectedCompFunction import connected_components
from functionsExperiment2 import convertCenter,get_distance, display_actual_centers,order, display_corrected_centers,display_predicted_centers
from kalmanFilter import init_kalman0
from bgSubFunction import BGSub
from datetime import datetime
import time
from xlwt import Workbook

def getVideos(foldername):

    acceptedFileExtensions = [".MOV", ".mp4", ".avi"]

    if not os.path.exists(foldername):
        print("No file")
        #valueSignal.logMessage("{} is not a File, please enter a correct file location containing videos".format(file))
        #return None

    file_names = os.listdir(foldername)
    print(file_names)
    videos = []

    for f in file_names:
        filename, file_extension = os.path.splitext(f)
        if file_extension in acceptedFileExtensions:
            videos.append(foldername + '/' + f)

    print(videos)

    if len(videos) < 1:
        print("No file")
        #valueSignal.logMessage("{} does not contain any valid files, please use from the following extensions: ".format(file))
        for ext in acceptedFileExtensions:
            print("{}".format(ext))

    return videos



    #for countVideo, fileName in enumerate(videos):
def mainApplication(fileName, display_video):

        cap = cv.VideoCapture(fileName)

        ############## REMEMBER - THIS METHOD WAS DONE USING THE FIRST FRAME OF THE VIDEO BUT NEED TO CHANGE THIS TO TAKE CLIP CHOSEN!!!!

        _, first_frame = cap.read()
        first_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)
        first_gray = cv.GaussianBlur(first_gray, (5, 5), 0)
        subtractor = cv.createBackgroundSubtractorMOG2(varThreshold=200, detectShadows=True)

        centers_list=[]
        centers_array = np.zeros((1,2),dtype = int)

        predictions0 = []
        corrected0_list = [np.zeros((2,1),dtype = int)]  # np.zeros((2,1),dtype = int)

        corrected0xcoords = []
        corrected0ycoords = []
        speed_list = []
        seconds_list = []

        kalman0 = init_kalman0()
        initial_once = 0

        # fps = cap.get(cv.cv.CV_CAP_PROP_FPS)
        # per video statistics
        trackingTimes = []  # total tracking times
        frame_num = -1  # current frame number
        height, width = first_frame.shape[:2]  # shape of video
        centerWidth = width / 2  # center width
        centerHeight = height / 2  # center height
        fps = np.math.ceil(cap.get(cv.cv2.CAP_PROP_FPS))  # frames per second

        # frameGroups = []  # frames determined to be tracking the drum
        totalFrameNumber = cap.get(cv.CAP_PROP_FRAME_COUNT)  # total number of frames in the video
        duration = float(totalFrameNumber) / float(fps)  # in seconds
        print(duration)

        #valueSignal.logMessage(str(datetime.now()))

        while True:

            frame_num = frame_num + 1
            _, frame = cap.read()
            frame_start_time = datetime.utcnow()

            seconds2 = float(frame_num) / float(fps)  # in seconds
            seconds = 1 / float(fps)  # in seconds
            seconds_list.append(seconds2)
            #print(seconds)

            if frame is None:
                print("Break {}".format(frame_num))
                break

            #frame, diff_mask = BGSub(frame, first_gray, subtractor, run_once, centers_list, kalman0, predictions0)

            frame = cv.GaussianBlur(frame, (5,5),0)

            gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            gray_frame = cv.GaussianBlur(gray_frame, (5, 5), 0)

            diff = cv.absdiff(first_gray, gray_frame)
            _, difference = cv.threshold(diff, 25, 255, cv.THRESH_BINARY)

            kernel = np.ones((5, 5), np.uint8)
            erode_diff = cv.erode(difference, None, iterations=5)

            mask = subtractor.apply(frame)
            mask[mask== 127] = 0

            diff_mask = np.bitwise_or(mask,erode_diff)

            centers, mask1 = connected_components(diff_mask)
            centers = np.array(centers)

            if centers != []:

                if initial_once == 0:
                    centers_list.append(centers)

                    initial_measurement0 = centers[0]

                    for count in range(20):
                        prediction0 = kalman0.predict()
                        prediction0 = prediction0[:2]
                        corrected0 = kalman0.correct(convertCenter(initial_measurement0))
                        predictions0.append(prediction0)
                        initial_once = 1

                end_component0 = order(predictions0, centers)

                corrected0 = kalman0.correct(convertCenter(centers[end_component0]))
                corrected02 = corrected0[:2]
                corrected0_list.append(corrected02)
                corrected0xcoords.append(corrected0[0])
                corrected0ycoords.append(corrected0[1])

                prediction0 = kalman0.predict()
                prediction0 = prediction0[:2]
                predictions0.append(prediction0)

                if display_video:
                    display_corrected_centers(corrected0,frame)
                    display_predicted_centers(prediction0,frame)
                    display_actual_centers(centers, frame)


            if len(corrected0_list)>1:

                distance = get_distance(corrected0_list[-2], corrected0_list[-1])
                speed = distance / seconds
                speed_list.append(speed)
            else:
                speed = 0
                speed_list.append(speed)

            if frame is None:
                print("Break {}".format(frame_num))
                break

            if display_video:
                window_capture_name = 'Video Capture'
                cv.namedWindow(window_capture_name, cv.WINDOW_NORMAL)
                cv.resizeWindow(window_capture_name, 600, 600)

                # window_detection_name = 'Object Detection'
                # cv.namedWindow(window_detection_name, cv.WINDOW_NORMAL)
                # cv.resizeWindow(window_detection_name, 600, 600)

                cv.imshow(window_capture_name, frame)
                #cv.imshow(window_detection_name, diff_mask)
                #print("Frame num:  {}".format(frame_num))

            if cv.waitKey(40) & 0xFF == ord('q'):
                break

        # duration = float(frame_num) / float(fps)  # in seconds
        # print(duration)

        cap.release()
        cv.destroyAllWindows()

        return corrected0xcoords, corrected0ycoords, speed_list, seconds_list




