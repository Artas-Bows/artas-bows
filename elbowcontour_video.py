import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print('Cannot open camera.')
    exit()

while True:

    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting.")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blank = np.zeros(frame.shape, dtype='uint8')
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (9, 9), 0)

    cv.imshow('Blur', blur)

    canny = cv.Canny(blur, 100, 125)

    contours, heirarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    for idx, contour in enumerate(contours):
        if len(contour) < 35: # 35 is the elbow.
            contours.pop(idx)

    print(f'{len(contours)} contour(s) found!')

    cv.drawContours(blank, contours, -1, (0, 255, 0), 1)

    cv.line(blank, (blank.shape[1] // 2, 0), (blank.shape[1] // 2, blank.shape[0]), (55, 55, 255), 1)

    bottomPoints = []
    pointsInContour = []

    for contour in contours:
        i = 0
        prevPoint = 0
        pInContour = 0
        lowest = [0, 0]

        for point in contour:
            i += 1
            if prevPoint == 0:
                pHigher = False
                if i != len(contour) and i != 1: #Makes sure that the point isn't at the beginning or end of the array so it doesn't go out of bounds
                    for x in range(i, len(contour)): #Here we check if there's a point anywhere on the right of the target point that is higher than the target point, if we encounter a lower point first then the loop breaks
                        if point[0][1] < contour[x][0][1]:
                            break
                        elif point[0][1] > contour[x][0][1]:
                            pHigher = True
                            break

                    if pHigher:
                        pHigher = False
                        for x in reversed(range(0, i - 1)):
                            #Checking if there's a point anywhere on the left that is higher, if there's a point that's lower, we break the loop
                            if point[0][1] < contour[x][0][1]:
                                pHigher = False
                                break
                            elif point[0][1] > contour[x][0][1]:
                                pHigher = True
                                break
                if pHigher:
                    prevPoint = 3
                    if pInContour == 0:
                        lowest = point[0]
                        pInContour = 1
                    pointsInContour.append(point[0])
            else:
                prevPoint -= 1

        finalPoints = []
        if lowest[0] != 0 and lowest[1] != 0:
            finalPoints.append(lowest)
            for point in pointsInContour:
                if lowest[1] > point[1]:
                    lowest = point
                    finalPoints.append(point)

        for point in finalPoints:
            bottomPoints.append(point)  

    for point in bottomPoints:
        cv.circle(blank, tuple(point), 1, (255, 0, 255), -1)

    print(f'Length of Array: {len(bottomPoints)}')

    cv.imshow('Contours', blank)

    if cv.waitKey(1) == ord('q'):
        break


cap.release()
cv.destroyAllWindows()