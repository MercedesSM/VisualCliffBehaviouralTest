# import the necessary packages
from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import imutils
import cv2 as cv
from connectedCompFunction import connected_components
from functionsExperiment2 import convertCenter,get_distance, display_actual_centers,order, display_corrected_centers,display_predicted_centers
from kalmanFilter import init_kalman0
import time
from findBoxFunction import findBox

# start the file video stream thread and allow the buffer to
# start to fill
def application(fileName,displayVideo):
    print("[INFO] starting video file thread...")
    fvs = FileVideoStream("{}".format(fileName)).start()
    time.sleep(1.0)
    # start the FPS timer
    fps = FPS().start()


    first_frame = fvs.read()

    height, width, channels = first_frame.shape
    width_resize = 450

    first_frame = imutils.resize(first_frame, width=width_resize)
    first_frame = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)
    first_frame = np.dstack([first_frame, first_frame, first_frame])

    first_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)
    first_gray = cv.GaussianBlur(first_gray, (5, 5), 0)
    subtractor = cv.createBackgroundSubtractorMOG2( varThreshold=200,detectShadows=True) # Turn off!!

    centers_list=[]

    predictions0 = []
    corrected0_list = [np.zeros((2,1),dtype = int)]

    corrected0xcoords = []
    corrected0ycoords = []
    sections = []
    secondslist = []
    speedlist = []
    cornersX = []
    cornersY = []

    kalman0 = init_kalman0()
    initial_once = 0
    findBoxOnce = 0
    frame_num = -1

    # loop over frames from the video file stream
    while fvs.more():
        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale (while still retaining 3
        # channels)
        frame = fvs.read()

        if frame is None:
            print("Break {}".format(frame_num))
            return corrected0xcoords, corrected0ycoords,sections, secondslist, speedlist, cornersX, cornersY


        resize_ratio = (width / width_resize)
        lefttopXR, quartertopXR, middletopXR, three_quartertopXR, righttopXR, cornersX, cornersY = findBox(frame, findBoxOnce, resize_ratio)

        frame_num = frame_num + 1

        frame = imutils.resize(frame, width=width_resize)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame = np.dstack([frame, frame, frame])

        frame = cv.GaussianBlur(frame, (5,5),0)

        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray_frame = cv.GaussianBlur(gray_frame, (5, 5), 0)

        diff = cv.absdiff(first_gray, gray_frame)
        _, difference = cv.threshold(diff, 25, 255, cv.THRESH_BINARY)

        kernel = np.ones((5, 5), np.uint8)
        #erode_diff = cv.erode(difference, None, iterations=3)
        opening = cv.morphologyEx(difference, cv.MORPH_OPEN, kernel)

        mask = subtractor.apply(frame)
        mask[mask== 127] = 0
        mask_dilate = cv.dilate(mask, None, iterations=3)

        diff_mask = np.bitwise_or(mask_dilate,opening)

        centers, mask1 = connected_components(diff_mask)

        if displayVideo:
            display_actual_centers(centers, frame)

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

            end_component0,missing = order(predictions0, centers)
            print(frame_num)

            corrected0 = kalman0.correct(convertCenter(centers[end_component0]))
            corrected02 = corrected0[:2]
            corrected0_list.append(corrected02)

            if len(corrected0_list) > 2:
                distance = get_distance(corrected0_list[-2], corrected0_list[-1])

                speed = distance / (secondslist[-1] - secondslist[-2])
                speedlist.append(speed)
            else:
                speed = 0
                speedlist.append(speed)

            if corrected0 is not None:
                if quartertopXR > corrected0[0] > lefttopXR:
                    section = 1
                    sections.append(section)

                if middletopXR > corrected0[0] > quartertopXR:
                    section = 2
                    sections.append(section)

                if three_quartertopXR > corrected0[0] > middletopXR:
                    section = 3
                    sections.append(section)

                if righttopXR > corrected0[0] > three_quartertopXR:
                    section = 4
                    sections.append(section)

            corrected0xcoords.append(corrected0[0])
            corrected0ycoords.append(corrected0[1])

            if missing == False:
                prediction0 = kalman0.predict()
                prediction0 = prediction0[:2]
                predictions0.append(prediction0)

                if displayVideo:
                    display_corrected_centers(corrected0,frame)
                    display_predicted_centers(prediction0,frame)

        else:
            if predictions0 == []:
                print("no predictions")
                corrected0xcoords.append(' ')
                corrected0ycoords.append(' ')
                speed = 0
                speedlist.append(speed)
                section = 0
                sections.append(section)
            else:

                # if it can not be seen, make the previous prediction the measured value
                first_prediction = predictions0[-1]
                first_prediction = first_prediction.tolist()
                first_prediction = first_prediction[0] + first_prediction[1]
                centers.append(first_prediction)

                end_component0, missing = order(predictions0, centers)
                print("there were predictions")

                corrected0 = kalman0.correct(convertCenter(centers[end_component0]))
                corrected02 = corrected0[:2]
                corrected0_list.append(corrected02)

                if len(corrected0_list) > 2:
                    distance = get_distance(corrected0_list[-2], corrected0_list[-1])

                    speed = distance / (secondslist[-1] - secondslist[-2])
                    speedlist.append(speed)
                else:
                    speed = 0
                    speedlist.append(speed)


                if corrected0 is not None:
                    if quartertopXR > corrected0[0] > lefttopXR:
                        section = 1
                        sections.append(section)

                    if middletopXR > corrected0[0] > quartertopXR:
                        section = 2
                        sections.append(section)

                    if three_quartertopXR > corrected0[0] > middletopXR:
                        section = 3
                        sections.append(section)

                    if righttopXR > corrected0[0] > three_quartertopXR:
                        section = 4
                        sections.append(section)

                else:
                    section = 0
                    sections.append(section)

                corrected0xcoords.append(corrected0[0])
                corrected0ycoords.append(corrected0[1])

                if displayVideo:
                    display_corrected_centers(corrected0, frame)
                    display_predicted_centers(prediction0, frame)

        if frame is None:
            print("Break {}".format(frame_num))
            return corrected0xcoords, corrected0ycoords,sections, secondslist, speedlist, cornersX, cornersY                             ##hmm

        if displayVideo:
            window_capture_name = 'Video Capture'
            cv.namedWindow(window_capture_name, cv.WINDOW_NORMAL)
            cv.resizeWindow(window_capture_name, 600, 600)

            window_detection_name = 'Object Detection'
            cv.namedWindow(window_detection_name, cv.WINDOW_NORMAL)
            cv.resizeWindow(window_detection_name, 600, 600)

            cv.imshow(window_capture_name, frame)
            cv.imshow(window_detection_name, diff_mask)

        fps.update()

        # stop the timer and display FPS information
        fps.stop()
        print(frame_num)
        sec = fps.elapsed()/fps.fps()
        secondslist.append(sec)

        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

        if cv.waitKey(40) & 0xFF == ord('q'):
            break

        # do a cleanup
    cv.destroyAllWindows()
    fvs.stop()
    return corrected0xcoords, corrected0ycoords,sections, secondslist, speedlist, cornersX, cornersY

def percentPerSection(sections, speed_list):
    time_percentages = []
    speed_averages = []
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    sumS1 = 0
    sumS2 = 0
    sumS3 = 0
    sumS4 = 0
    total_sections = len(sections)
    for i, section in enumerate(sections):
        if section == 1:
            sumS1 += speed_list[i]
            count1 += 1
        if section == 2:
            sumS2 += speed_list[i]
            count2 += 1
        if section == 3:
            sumS3 += speed_list[i]
            count3 += 1
        if section == 4:
            sumS4 += speed_list[i]
            count4 += 1
    time1 = (count1 / total_sections) * 100
    time2 = (count2 / total_sections) * 100
    time3 = (count3 / total_sections) * 100
    time4 = (count4 / total_sections) * 100

    time_percentages.append(time1)
    time_percentages.append(time2)
    time_percentages.append(time3)
    time_percentages.append(time4)

    averageS1 = sumS1 / count1
    averageS2 = sumS2 / count2
    averageS3 = sumS3 / count3
    averageS4 = sumS4 / count4

    speed_averages.append(averageS1)
    speed_averages.append(averageS2)
    speed_averages.append(averageS3)
    speed_averages.append(averageS4)

    return time_percentages, speed_averages

