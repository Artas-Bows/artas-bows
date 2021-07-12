import cv2 as cv
import numpy as np

def rescaleFrame(frame, scale = 0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width,height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


img = cv.imread('Picture/pointing3.jpg')
cv.imshow('Image', img)

resized_image = rescaleFrame(img, scale = 0.4)

blank = np.zeros(resized_image.shape, dtype='uint8')

gray = cv.cvtColor(resized_image, cv.COLOR_BGR2GRAY)

blur = cv.GaussianBlur(gray, (9,9), 0)
cv.imshow('Blur', blur)

canny = cv.Canny(blur, 100, 125)

contours, heirarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

ind = 0
for contour in contours:
    if (len(contour)<35):
        contours.pop(ind)
    ind+=1
        

#print(f'Contour: {contours[35]}')
print(f'{len(contours)} contour(s) found!')
#print(f'PointY: {contours[1][1][0][1]}')

#for i in range(8,10):
#   cv.drawContours(blank, contours, i, (0,255,0), 2)

cv.drawContours(blank, contours, -1, (0,255,0), 1) #35 is the elbow

# for contour in contours:
#     i = 0
#     for point in contour:
#         i+=1
#         if(i!=len(contour) and i!=1):
#             if((abs(point[0][1]-contour[i][0][1])>5) or (abs(point[0][1]-contour[i-2][0][1])>5) and (abs(point[0][0]-contour[i][0][0])>7) or (abs(point[0][0]-contour[i-2][0][0])>7)):
#                 cv.circle(blank, point[0], 2, (255, 0,255), -1)

cv.line(blank, (blank.shape[1]//2, 0),(blank.shape[1]//2, blank.shape[0]), (55, 55,255), 1)

bottomPoints = []
pointsInContour = []

for contour in contours:
    i = 0
    prevPoint = 0
    pInContour = 0
    lowest = [0, 0]

    for point in contour:
        i+=1
        if(prevPoint == 0):
            pHigher = False
            if(i!=len(contour) and i!=1): #Makes sure that the point isn't at the beginning or end of the array so it doesn't go out of bounds
                for x in range(i,len(contour)): #Here we check if there's a point anywhere on the right of the target point that is higher than the target point, if we encounter a lower point first then the loop breaks
                    if(point[0][1]<contour[x][0][1]):
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
    if(lowest[0] != 0 and lowest[1] != 0):
        finalPoints.append(lowest)
        for point in pointsInContour:
            if(lowest[1]>point[1]):
                lowest = point
                finalPoints.clear
                finalPoints.append(point)
        
    for point in finalPoints:
        bottomPoints.append(point)
    #Check for lowest point in contour and add that to bottompoints, probably don't need to sort can just go through each point and set variable for lowest in array

            
    
#y_threshold = 10 #Distance between two points' y values must be greater than this
#x_threshold = 5  #Distance between two points' x values must be less than this

# i=0
# for point in bottomPoints:
#     i+=1
#     if(i!=len(bottomPoints)):
#         if((abs(bottomPoints[i][1]-point[1])>y_threshold) and (abs(bottomPoints[i][0]-point[0])<x_threshold)):
#             cv.circle(blank, point, 1, (255, 0,255), -1)
        
    
# i=0
# for point in bottomPoints:
#     i+=1
#     if(i!=len(bottomPoints)):
#         if((abs(bottomPoints[i][1]-point[1])<10) and (abs(bottomPoints[i][0]-point[0])<5)):
#             bottomPoints.pop(i)

for point in bottomPoints:
    cv.circle(blank, point, 1, (255, 0,255), -1)
            
print(f'Length of Array: {len(bottomPoints)}')



# for contour in contours:
#     for point in contour:
#         cv.circle(blank, point[0], 1, (255, 0,255), -1)


cv.imshow('Contours', blank)

cv.waitKey(0)