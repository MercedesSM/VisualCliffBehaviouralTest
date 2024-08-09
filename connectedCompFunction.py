import cv2 as cv
import numpy as np
from imutils import grab_contours, contours
from skimage import measure
import math

def connected_components(threshold):

    kernel = np.ones((5, 5), np.uint8) #the size of errotion and dilation
    opening = cv.morphologyEx(threshold, cv.MORPH_OPEN, kernel) #is erroding then dilating in one

    # Connected components when they are neighbors and have the same value
    # neighbors=8 means have to share only edge or vertex
    # background = 0 considers all pixels with that value as background pixels and labels them as 0
    labels = measure.label(opening, neighbors=8, background=0)

    # initialize a mask to store only the large components
    mask = np.zeros(opening.shape, dtype="uint8")

    # loop over the unique components
    for label in np.unique(labels):
        # if this is the background label, ignore it
        if label == 0:
            continue

        # otherwise,
        # construct the label mask
        label_mask = np.zeros(opening.shape, dtype="uint8")
        label_mask[labels == label] = 255

        # count the number of pixels (returns the number of non-zero elements)
        numPixels = cv.countNonZero(label_mask)

        # if number of pixels large enough, then add to mask (where storing only the large components)
        if numPixels > 200:
            mask = cv.add(mask, label_mask)

    #find the contours in the mask
    contours = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    #grab contours from the find contours function above, makes it into a list
    contours = grab_contours(contours)

    # contours sorted by size (largest first)
    sorted_contours = sorted(contours, key=lambda x: cv.contourArea(x))

    # contours = contours.sort_contours(contours)[0]
    #print("Number of contours detected %d ->" % len(contours))

    centers=[]
    # loop over the contours, find the center points
    for c in sorted_contours:
        M = cv.moments(c)

        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        centers.append([cX, cY])
        
    return centers, mask


