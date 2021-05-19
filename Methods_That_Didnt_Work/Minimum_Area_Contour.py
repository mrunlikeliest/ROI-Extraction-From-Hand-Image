import cv2
import numpy as np

#reading image
img1= cv2.imread("016_2.jpg")
#resizing for convenience
scale_percent=50
width=int(img1.shape[1]*scale_percent/100)
height= int(img1.shape[0]*scale_percent/100)
dim=(width,height)

img=cv2.resize(img1, dim, interpolation=cv2.INTER_AREA)

cv2.imshow("img", img)

#convert image to BGR
img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#skin color range for hsv_value
HSV_mask = cv2.inRange(img_HSV, (35, 36, 20), (179,255,255))
HSV_mask = cv2.morphologyEx(HSV_mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))

HSV_result = cv2.bitwise_not(HSV_mask)

#show results
cv2.imshow("1_hsv.jpg", HSV_result)

#binary thresholding
_, th1= cv2.threshold(HSV_result, 100, 255, cv2.THRESH_BINARY)
cv2.imshow("th1", th1)

#canny edge detection
canny= cv2.Canny(th1, 100,200)
cv2.imshow("canny_edge", canny)

#contour detection
contours, hierarchy= cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#color=[[255,0,0],[0,255,0],[0,0,255],[255,255,255],[255,255,0],[255,0,255],[0,255,255],[170,170,0],[134,199,200],[100,100,100],[167,87,205]]
#i=0
for cnt in contours:
#get minimum inclosing circle
    #(x,y), radius=cv2.minEnclosingCircle(cnt)
    #center=(int(x), int (y))
    #radius=int(radius)
    #cont1=cv2.circle(img, center, radius, (255,0,0),2)
#bounding rectangle
    #x,y,w,h=cv2.boundingRect(cnt)
    #cont=cv2.rectangle(img,(x,y),(x+w,y+h), (255,0,0), 2)
    #trying to draw minimum rectangular contours
    rect=cv2.minAreaRect(cnt)
    box=cv2.boxPoints(rect)
    box=np.int0(box)
    area=cv2.contourArea(cnt)
    #print(area)
    if area>11:
        x,y,w,h=cv2.boundingRect(cnt)
        #print(w,h)
#trying to drawContours using approxpolydp
    #epsilon=0.01*cv2.arcLength(cnt,True)
    #approx=cv2.approxPolyDP(cnt, epsilon, True)
        cont=cv2.drawContours(img, [box], 0, (255,0,255), 2)
        #i=i+1
#cv2.imshow("cont",cont)
cv2.imshow("cont",cont)


#finding fingertip using minarearect() contours


cv2.waitKey(0)
cv2.destroyAllWindows()
