import cv2 as cv
import numpy as np


def convertCenter(center):
    return np.array([[np.float32(center[0])],[np.float32(center[1])]])

def getlength(x1, y1, x2, y2):
    return np.math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def get_distance(point1, point2):
    return np.math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def order(predictions, measurements):
    component = -1
    distance = -1
    components_picked = []
    radius = 50
    missing = False

    for number, measurement in enumerate(measurements):
            prediction = predictions[-1]

            new_distance = get_distance(prediction, measurement)

            if (component == -1 or new_distance < distance) and number not in components_picked:
                    distance = new_distance
                    component = number
                    components_picked.append(component)

    if distance > radius:
        missing = True

        #if it reaches this then the next prediction should still be this value --- don't predict???
        component = -1
        distance = -1
        components_picked = []

        first_prediction = predictions[-1]
        first_prediction = first_prediction.tolist()
        first_prediction = first_prediction[0] + first_prediction[1]
        measurements.append(first_prediction)

        for number, measurement in enumerate(measurements):

            new_distance = get_distance(first_prediction, measurement)

            if (component == -1 or new_distance < distance) and number not in components_picked:
                distance = new_distance
                component = number
                components_picked.append(component)

    end_component = components_picked[-1]
    return end_component,missing

def display_actual_centers(centers, frame):
    for number, center in enumerate(centers):

        centerX = center[0]
        centerY = center[1]

        # Draw Actual points from thresholding
        cv.circle(frame, (centerX, centerY), 5, [0, 0, 255], 2, 8)
        cv.putText(frame, "Actual", (0, 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, [0, 0, 255])


def display_corrected_centers(corrected, frame):
    cv.circle(frame, (corrected[0], corrected[1]), 5, [0, 255, 255], 2, 8)
    cv.putText(frame, "Corrected", (0, 25), cv.FONT_HERSHEY_SIMPLEX, 0.5,[0, 255, 255])

def display_predicted_centers(predicted, frame):
    cv.circle(frame, (predicted[0], predicted[1]), 5, [255, 0, 0], 2, 8)
    cv.putText(frame, "Predicted", (0, 40), cv.FONT_HERSHEY_SIMPLEX, 0.5,[255, 0, 0])



