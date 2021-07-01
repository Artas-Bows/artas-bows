import cv2 as cv
import numpy as np
from operator import itemgetter

img = cv.imread('Picture/pointing3.jpg')
cv.imshow('Image', img)

blank = np.zeros(img.shape, dtype='uint8')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

blur = cv.GaussianBlur(gray, (11,11), 0)
#blur = cv.bilateralFilter(gray, 15, 45, 35)
cv.imshow('Blur', blur)

canny = cv.Canny(blur, 100, 125)

contours, heirarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
#print(f'Contour: {contours[35]}')
print(f'{len(contours)} contour(s) found!')
#print(f'PointY: {contours[1][1][0][1]}')

#for i in range(36,37):
#    cv.drawContours(blank, contours, i, (0,255,0), 2)

cv.drawContours(blank, contours, -1, (0,255,0), 1) #35 is the elbow

# for contour in contours:
#     i = 0
#     for point in contour:
#         i+=1
#         if(i!=len(contour) and i!=1):
#             if((abs(point[0][1]-contour[i][0][1])>5) or (abs(point[0][1]-contour[i-2][0][1])>5) and (abs(point[0][0]-contour[i][0][0])>7) or (abs(point[0][0]-contour[i-2][0][0])>7)):
#                 cv.circle(blank, point[0], 2, (255, 0,255), -1)

bottomPoints = []

for contour in contours:
    i = 0
    prevPoint = 0 

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
                prevPoint = 1 #If a point is found that matches our criteria, the next x points will not even be checked so that we don't get point clusters
                bottomPoints.append(point[0])
        else:
            prevPoint-=1


            
    
y_threshold = 40 #Distance between two points' y values must be greater than this
x_threshold = 5  #Distance between two points' x values must be less than this

bottomPoints.sort(key=itemgetter(0))

newArray = []

# i=0
# for point in bottomPoints:
#     i+=1
#     if(i!=len(bottomPoints)):
#         if((bottomPoints[i][0]-point[0]<x_threshold) and abs(bottomPoints[i][1]-point[1]>y_threshold)):
#             newArray.append(point)
#             newArray.append(bottomPoints[i])

print(f'Length of New Array: {len(newArray)}')

for point in newArray:
    cv.circle(blank, point, 1, (255, 0,255), -1)


print(f'Length of Array: {len(bottomPoints)}')

# i=0
# for point in bottomPoints:
#     i+=1
#     if(i!=len(bottomPoints)):
#         if((abs(bottomPoints[i][1]-point[1])>y_threshold) and (abs(bottomPoints[i][0]-point[0])<x_threshold)):
#             cv.circle(blank, point, 1, (255, 0,255), -1)
        
    

            




# for contour in contours:
#     for point in contour:
#         cv.circle(blank, point[0], 1, (255, 0,255), -1)


cv.imshow('Contours', blank)

cv.waitKey(0)