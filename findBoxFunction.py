import cv2 as cv
import numpy as np
from imutils import grab_contours
from skimage import measure
import math

def findBox(frame, findBoxOnce, resize_ratio):
    if findBoxOnce == 0:
        frame_copy = frame.copy()
        gray = cv.cvtColor(frame_copy, cv.COLOR_BGR2GRAY)

        _,threshold = cv.threshold(gray, 150,255,cv.THRESH_BINARY)

        kernel = np.ones((5, 5), np.uint8)  # the size of errotion and dilation
        opening = cv.morphologyEx(threshold, cv.MORPH_OPEN, kernel)  # is erroding then dilating in one

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
            if numPixels > 2000:
                mask = cv.add(mask, label_mask)

        # find the contours in the mask
        contours = cv.findContours(mask.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # grab contours from the find contours function above, makes it into a list
        contours = grab_contours(contours)

        c = max(contours, key=cv.contourArea)
        #cv.drawContours(frame_copy, [c], -1, (0, 0, 255), cv.FILLED)
        #cv.drawContours(frame, contours, -1, (255, 0, 0), cv.FILLED)

        perimeter = cv.arcLength(c, True)
        epsilon = 0.02 * perimeter
        approximation = cv.approxPolyDP(c, epsilon, True)
        x, y, w, h = cv.boundingRect(approximation)
        rectangle = (x, y, w, h)
        #cv.rectangle(frame_copy, (x, y), (x+w, y+h), (255, 0, 0), 1)        #####copy
        centerX = math.floor(x + (w/2))
        centerY = math.floor(y + (h/2))

        quartertopX = math.floor(x+w/4)         ## 1, 4
        quartertopY = math.floor(y + h/4)
        quarterbottomX = math.floor(x+w/4)
        quarterbottomY = math.floor(h + y/4)

        middletopX = math.floor(x+w/2)              ## 3, 6
        middletopY = math.floor(y + h/2)
        middlebottomX = math.floor(x+w/2)
        middlebottomY = math.floor(h + y/2)

        three_quartertopX = math.floor(x+3*w/4)     ## 5, 8
        three_quartertopY = math.floor(y + 3*h/4)
        three_quarterbottomX = math.floor(x+3*w/4)
        three_quarterbottomY = math.floor(h + 3*y/4)

        lefttopX = math.floor(x) #(w / 2)               ## 2
        lefttopY = math.floor(y) #+ (h / 2)
        leftbottomX = math.floor(x)
        leftbottomY = math.floor(h)

        righttopX = math.floor(x+w) #(w / 2)            ## 7
        righttopY = math.floor(y+h) #+ (h / 2)
        rightbottomX = math.floor(x+w)
        rightbottomY = math.floor(y)

        lefttopXR = lefttopX/resize_ratio
        quartertopXR = quartertopX/resize_ratio
        middletopXR = middletopX/resize_ratio
        three_quartertopXR = three_quartertopX/resize_ratio
        righttopXR = righttopX/resize_ratio

        leftbottomXR = leftbottomX/resize_ratio
        rightbottomXR = rightbottomX/resize_ratio

        lefttopYR = lefttopY/resize_ratio
        righttopYR= righttopY/resize_ratio
        leftbottomYR= leftbottomY/resize_ratio
        rightbottomYR= rightbottomY/resize_ratio

        findBoxOnce +=1

        cornersX = [lefttopXR,righttopXR,leftbottomXR,rightbottomXR]
        cornersY = [lefttopYR, righttopYR, leftbottomYR,rightbottomYR]

        # corners.append(leftTopCorner)
        # corners.append(rightTopCorner)
        # corners.append(leftBottomCorner)
        # corners.append(rightBottomCorner)

        # ## Each corner
        # cv.circle(frame_copy, (lefttopX, lefttopY), 10, (0,0,255), thickness=5)
        # cv.circle(frame_copy, (leftbottomX, leftbottomY), 10, (0, 0, 255), thickness=5)
        # cv.circle(frame_copy, (righttopX, righttopY), 10, (0, 0, 255), thickness=5)
        # cv.circle(frame_copy, (rightbottomX, rightbottomY), 10, (0, 0, 255), thickness=5)
        #
        # cv.circle(frame_copy, (centerX, centerY), 10, (0, 0, 255), thickness=2)
        #
        # # Line 1
        # cv.line(frame_copy, pt1=(lefttopX, 0), pt2=(leftbottomX, leftbottomY), color=(255, 0, 0), thickness=5)
        # # Line 2
        # cv.line(frame_copy, pt1=(quartertopX, 0), pt2=(quarterbottomX, quarterbottomY), color=(255, 0, 0), thickness=5)
        # # Line 3
        # cv.line(frame_copy, pt1=(middletopX, 0), pt2=(middlebottomX, middlebottomY), color=(255, 0, 0), thickness=5)
        # # Line 4
        # cv.line(frame_copy, pt1=(righttopX, 0), pt2=(rightbottomX, middlebottomY), color=(255, 0, 0), thickness=5)
        # # Line 5
        # cv.line(frame_copy, pt1=(three_quartertopX, 0), pt2=(three_quarterbottomX, three_quarterbottomY), color=(255, 0, 0), thickness=5)


        #cv.line(frame, pt1=(lefttopX, middletopY), pt2=(righttopX, middletopY), color=(0, 255, 0), thickness=2)

        #cv.drawContours(frame, [c], -1, (0, 255, 0), 8)

        return lefttopXR, quartertopXR, middletopXR, three_quartertopXR, righttopXR, cornersX, cornersY