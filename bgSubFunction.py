import cv2 as cv
import numpy as np
import os.path
from connectedCompFunction import connected_components
from functionsExperiment2 import convertCenter,get_distance, display_actual_centers,order, display_corrected_centers,display_predicted_centers
from kalmanFilter import init_kalman0

def BGSub(frame, first_gray,subtractor, run_once, centers_list, kalman0, predictions0):

        frame = cv.GaussianBlur(frame, (5, 5), 0)

        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray_frame = cv.GaussianBlur(gray_frame, (5, 5), 0)

        diff = cv.absdiff(first_gray, gray_frame)
        _, difference = cv.threshold(diff, 25, 255, cv.THRESH_BINARY)

        kernel = np.ones((5, 5), np.uint8)
        erode_diff = cv.erode(difference, None, iterations=5)

        mask = subtractor.apply(frame)
        mask[mask == 127] = 0

        diff_mask = np.bitwise_or(mask, erode_diff)

        centers, mask1 = connected_components(diff_mask)
        centers = np.array(centers)

        if centers != []:

            if run_once == 0:
                centers_list.append(centers)

                initial_measurement0 = centers[0]

                for count in range(20):
                    prediction0 = kalman0.predict()
                    prediction0 = prediction0[:2]
                    corrected0 = kalman0.correct(convertCenter(initial_measurement0))
                    predictions0.append(prediction0)
                    run_once = 1

            end_component0 = order(predictions0, centers)

            corrected0 = kalman0.correct(convertCenter(centers[end_component0]))
            prediction0 = kalman0.predict()
            prediction0 = prediction0[:2]
            predictions0.append(prediction0)

            display_corrected_centers(corrected0, frame)
            display_predicted_centers(prediction0, frame)

        display_actual_centers(centers, frame)
        return frame, diff_mask
