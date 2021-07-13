import cv2 as cv
import numpy as np

def rescaleFrame(frame, scale = 0.75): #Resizes an image or video, not my code so I'm not that sure how it works, refer to tutorial for better explanation
    width = int(frame.shape[1] * scale) #frame.shape[1] is the original width of our image
    height = int(frame.shape[0] * scale) #frame.shape[0] is the original height of our image
    dimensions = (width,height) 

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


img = cv.imread('Picture/pointing3.jpg')
cv.imshow('Image', img)

resized_image = rescaleFrame(img, scale = 0.4) #Resizes the image using the rescaleFrame function

blank = np.zeros(resized_image.shape, dtype='uint8') #Creates an empty placeholder image that is the same size as our image, this is used for drawing the contours and circles and stuff. This can also be used as a mask

gray = cv.cvtColor(resized_image, cv.COLOR_BGR2GRAY) #Sets the image to gray scale

blur = cv.GaussianBlur(gray, (9,9), 0) #Blurs the image using GaussianBlur, other blurring algorithms might work better, needs for testing
cv.imshow('Blur', blur)

canny = cv.Canny(blur, 100, 125) #This takes in the resized, blurred, gray image and sets the edges for the image, this step could be skipped, have to do some testing

contours, heirarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE) #This gives us a 4 fucking dimensional list of all the contours, the heirarchies variable gives us the contours that are within other contours, not sure what that's really used for yet

ind = 0
for contour in contours: #We don't want small contours, the elbow is going to be a pretty large contour every time so it's not worth even checking the small ones most of the time
    if (len(contour)<35):
        contours.pop(ind)
    ind+=1
        
print(f'{len(contours)} contour(s) found!')
#print(f'PointY: {contours[1][1][0][1]}') 

#for i in range(8,10):
#   cv.drawContours(blank, contours, i, (0,255,0), 2)

cv.drawContours(blank, contours, -1, (0,255,0), 1) #draws all the contours onto our blank image

cv.line(blank, (blank.shape[1]//2, 0),(blank.shape[1]//2, blank.shape[0]), (55, 55,255), 1) #Draws a line through the middle of the image, this would in theory be where the pong table would be

bottomPoints = [] #This is the final list of elbow points

for contour in contours:
    i = 0
    pointsInContour = [] #List of all the elbow points that were detected in a contour, this list is then dwindled down to the finalPoints list where we have just the lowest points from the pointsInContour list
    prevPoint = 0 #When we detect an elbow point, this value is set to 3, this results in the algorithm skipping the next three points so we don't get bunches of points all together.
    pInContour = 0 #This is just used to keep track of which elbow point is the first discovered in each contour, if this is set to 0 when an elbow point is detected, this is set to 1.
    lowest = [-1, -1] #This is a point that is initially set to the first discovered elbow point in a contour, it's then compared to the rest of the elbow points that are discovered in order to find the lowest y-value of all the elbow points in a contour, only the points that are at this y-value are added to the bottomPoints array.

    for point in contour:
        i+=1
        if(prevPoint == 0): #Checks if there was an elbow point in the last three points
            pHigher = False #If we make it to the end of this for loop and this is False, that means we didn't get a bottom point and we go to check the next point in the contour. If it's set to True, we add it to the pointsInContour array
            if(i!=len(contour) and i!=1): #Makes sure that the point isn't at the beginning or end of the array so it doesn't go out of bounds
                for x in range(i,len(contour)): #In this loop we check if there's a point anywhere on the right of the target point that is higher than the target point, if we encounter a lower point first then the loop breaks
                    if(point[0][1]<contour[x][0][1]): #For some reason, each point is in its own 2D array so we have to do point[0] to get the actualy point. ex: point[0] would give you something like [4,19] but the point variable would give you [[4,19]]
                        break
                    elif(point[0][1]>contour[x][0][1]):
                        pHigher = True
                        break

                if(pHigher):
                    pHigher = False
                    for x in reversed(range(0,i-1)):
                        if(point[0][1]<contour[x][0][1]): #Checking if there's a point anywhere on the left that is higher, if there's a point that's lower, we break the loop
                            pHigher = False
                            break
                        elif(point[0][1]>contour[x][0][1]):
                            pHigher = True
                            break
            if(pHigher):
                prevPoint = 3
                if(pInContour == 0):
                    lowest = point[0]
                    pInContour=1
                pointsInContour.append(point[0])
        else:
            prevPoint-=1
    
    finalPoints = []
    if(lowest[0] != -1 and lowest[1] != -1): #Makes sure lowest isn't set to the default value of [-1,-1], in which case, there were no points in the array
        finalPoints.append(lowest)
        for point in pointsInContour:
            if(lowest[1]<point[1]): #The higher the y-value, the lower the point is in the actual image
                lowest = point
                finalPoints.clear #If there's a point that's lower than our lowest variable, we set the new lowest to that point and clear the array since the old values are at the previous y-value
                finalPoints.append(point)
        
    for point in finalPoints:
        bottomPoints.append(point)
    #Check for lowest point in contour and add that to bottompoints, probably don't need to sort can just go through each point and set variable for lowest in array
        
    

for point in bottomPoints:
    cv.circle(blank, point, 1, (255, 0,255), -1) #Creates a pink circle at every elbow point
            
print(f'Length of Array: {len(bottomPoints)}') 



cv.imshow('Contours', blank)

cv.waitKey(0)