import numpy as np
import cv2 as cv

def skinmask(img):
    hsvim = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower = np.array([35, 45, 20], dtype = "uint8")
    upper = np.array([179, 255, 255], dtype = "uint8")
    skinRegionHSV = cv.inRange(hsvim, lower, upper)
    hsv_res=cv.bitwise_not(skinRegionHSV)
    blurred = cv.blur(hsv_res, (2,2))
    ret, thresh = cv.threshold(blurred,0,255,cv.THRESH_BINARY)
    cv.imshow("thresh",thresh)
    return thresh

def getcnthull(mask_img):
    contours, hierarchy = cv.findContours(mask_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = max(contours, key=lambda x: cv.contourArea(x))
    hull = cv.convexHull(contours)
    return contours, hull

def getdefects(contours):
    hull = cv.convexHull(contours, returnPoints=False)
    defects = cv.convexityDefects(contours, hull)
    return defects

def getcenter(contours):
    m=cv.moments(contours)
    cx=int(m["m10"]/m["m00"])
    cy=int(m["m01"]/m["m00"])
    return cx,cy

#reading image
img1= cv.imread("001_1.jpg")
#resizing for convenience
scale_percent=40
width=int(img1.shape[1]*scale_percent/100)
height= int(img1.shape[0]*scale_percent/100)
dim=(width,height)

img=cv.resize(img1, dim, interpolation=cv.INTER_AREA)

lst=[]
try:
    mask_img = skinmask(img)
    contours, hull = getcnthull(mask_img)
    #circle=cv2.circle(img, (cx, cy), 5, (255, 0, 255), -1)
    #cv2.imshow("circles",circle)
    cx,cy=getcenter(contours)
    print(cx,cy)
    a1=cx-50
    b1=cy-40
    a2=cx+100
    b2=cy+110
    print(a1,b1,a2,b2)
    palm=cv.rectangle(img,(a1,b1),(a2,b2),(0,0,0),1)
    cv.circle(img,(cx,cy),1,(255,0,255),2)
    cv.drawContours(img, [contours], -1, (0,255,255), 2)
    cv.drawContours(img, [hull], -1, (255, 255, 255), 2)
    defects = getdefects(contours)
    #print(defects)
    if defects is not None:
        cnt = 0
        k=0
        for i in range(defects.shape[0]):
             # calculate the angle
            s, e, f, d = defects[i][0]
            start = tuple(contours[s][0])
            end = tuple(contours[e][0])
            far = tuple(contours[f][0])
            a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
            angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  #      cosine theorem
            if angle <= np.pi / 2:  # angle less than 90 degree, treat as fingers
                cnt += 1
                rang=[(0,0,0),(255,0,0),(0,255,0),(255,255,255)]
                print(k)
                print(rang[k])
                cv.circle(img, far, 4, rang[k], -1)
                #print("start:",start)
                #print("end:",end)
                #making rectangles
                cv.circle(img,start,5,[0,0,0],-1)
                cv.circle(img,end,5,[0,255,0],-1)
                #a=start
                x1=start[0]-20
                y1=start[1]
                x2=x1+40
                y2=y1+30
                ex=cv.rectangle(img, (x1,y1),(x2,y2),(0,0,0),1)
                #roi=img[x1:x2,y1:y2]
                #cv.imshow("roi",roi)
                k+=1
        if cnt > 0:
            cnt = cnt+1
        cv.putText(img, str(cnt), (0, 50), cv.FONT_HERSHEY_SIMPLEX,1, (255, 0, 0) , 2, cv.LINE_AA)
    cv.imshow("img", img)

except:
    pass
#if cv.waitKey(1) & 0xFF == ord('q'):
    #break
cv.waitKey(0)
cv.destroyAllWindows()
