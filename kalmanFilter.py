import cv2 as cv
import numpy as np

# Kalman filter models a system and estimates its internal state
# measuring only input and output
def init_kalman0():

    #init kalman - (dynamParams, measureParams)
    kalman0 = cv.KalmanFilter(4, 2)

    # ************************** Predict ******************************

    # Updates last known estimate of state to reflect the current state
    # This prediction matrix uses kinematic formula to give us the next state
    kalman0.transitionMatrix = np.array([[1, 0, 1, 0],
                                         [0, 1, 0, 1],
                                         [0, 0, 1, 0],
                                         [0, 0, 0, 1]], np.float32)

    # Noise that represents error in the system (uncertainties)
    kalman0.processNoiseCov = np.array([[1, 0, 0, 0],
                                        [0, 1, 0, 0],
                                        [0, 0, 1, 0],
                                        [0, 0, 0, 1]], np.float32) * 0.3

    # ************************** Update ******************************

    # Observation matrix - transforms our current estimate of state
    # to best estimate of system output (relates measurement and state)
    # only x and y position observed (not x and y velocity)
    kalman0.measurementMatrix = np.array([[1, 0, 0, 0],
                                         [0, 1, 0, 0]], np.float32)

    return kalman0


def init_kalman1():

    kalman1 = cv.KalmanFilter(4, 2)

    kalman1.measurementMatrix = np.array([[1, 0, 0, 0],
                                         [0, 1, 0, 0]], np.float32)

    kalman1.transitionMatrix = np.array([[1, 0, 1, 0],
                                        [0, 1, 0, 1],
                                        [0, 0, 1, 0],
                                        [0, 0, 0, 1]], np.float32)

    kalman1.processNoiseCov = np.array([[1, 0, 0, 0],
                                       [0, 1, 0, 0],
                                       [0, 0, 1, 0],
                                       [0, 0, 0, 1]], np.float32) * 0.3
    return kalman1


def init_kalman2():

    kalman2 = cv.KalmanFilter(4, 2)

    kalman2.measurementMatrix = np.array([[1, 0, 0, 0],
                                         [0, 1, 0, 0]], np.float32)

    kalman2.transitionMatrix = np.array([[1, 0, 1, 0],
                                        [0, 1, 0, 1],
                                        [0, 0, 0, 0],
                                        [0, 0, 0, 0]], np.float32)

    kalman2.processNoiseCov = np.array([[1, 0, 0, 0],
                                       [0, 1, 0, 0],
                                       [0, 0, 1, 0],
                                       [0, 0, 0, 1]], np.float32) * 0.3
    return kalman2



def init_kalman(dt):

    kalman = cv.KalmanFilter(4, 2)

    kalman.transitionMatrix = np.array([[1, 0, dt, 0],
                                         [0, 1, 0, dt],
                                         [0, 0, 1, 0],
                                         [0, 0, 0, 1]], np.float32)


    kalman.processNoiseCov = np.array([[1, 0, 0, 0],
                                        [0, 1, 0, 0],
                                        [0, 0, 1, 0],
                                        [0, 0, 0, 1]], np.float32) * 0.3

    kalman.measurementMatrix = np.array([[1, 0, 0, 0],
                                         [0, 1, 0, 0]], np.float32)

    return kalman

