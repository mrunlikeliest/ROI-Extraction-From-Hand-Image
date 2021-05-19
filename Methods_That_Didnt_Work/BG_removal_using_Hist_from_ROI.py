import cv2
import numpy as np

#declaring var to be used
hand_hist = None
traverse_point = []
total_rectangle = 9
hand_rect_one_x = None
hand_rect_one_y = None

hand_rect_two_x = None
hand_rect_two_y = None

img1= cv2.imread("001_1.jpg")
#resizing for convenience
scale_percent=40
width=int(img1.shape[1]*scale_percent/100)
height= int(img1.shape[0]*scale_percent/100)
dim=(width,height)

img=cv2.resize(img1, dim, interpolation=cv2.INTER_AREA)


#making rectangles
rows, cols, _ = img.shape
print(rows,cols)
#global total_rectangle, hand_rect_one_x, hand_rect_one_y, hand_rect_two_x, hand_rect_two_y
hand_rect_one_x = np.array(
    [16 * rows / 20, 16 * rows / 20, 16 * rows / 20, 19 * rows / 20, 19 * rows / 20, 19 * rows / 20, 12 * rows / 20,
        12 * rows / 20, 12 * rows / 20], dtype=np.uint32)

hand_rect_one_y = np.array(
    [11 * cols / 20, 12 * cols / 20, 13 * cols / 20, 11 * cols / 20, 12 * cols / 20, 13 * cols / 20, 11 * cols / 20,
        12 * cols / 20, 13 * cols / 20], dtype=np.uint32)

hand_rect_two_x = hand_rect_one_x + 50
hand_rect_two_y = hand_rect_one_y + 50
#print(hand_rect_two_x)

for i in range(total_rectangle):
    ex=cv2.rectangle(img, (hand_rect_one_y[i], hand_rect_one_x[i]),
                     (hand_rect_two_y[i], hand_rect_two_x[i]),
                     (0, 0, 0), 1)
    break
    cv2.imshow("extract",ex)

#hand histogram
hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
roi = np.zeros([90, 10, 3], dtype=hsv_frame.dtype)

for i in range(total_rectangle):
    roi[i * 10: i * 10 + 10, 0: 10] = hsv_frame[hand_rect_one_x[i]:hand_rect_one_x[i] + 10,
                                         hand_rect_one_y[i]:hand_rect_one_y[i] + 10]

hand_hist = cv2.calcHist([roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
norm=cv2.normalize(hand_hist, hand_hist, 0, 255, cv2.NORM_MINMAX)
#cv2.imshow('norm',norm)

#call back project
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
dst = cv2.calcBackProject([hsv], [0, 1], hand_hist, [0, 180, 0, 256], 1)

disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
cv2.filter2D(dst, -1, disc, dst)

ret, thresh = cv2.threshold(dst, 150, 255, cv2.THRESH_BINARY)

thresh = cv2.merge((thresh, thresh, thresh))

final=cv2.bitwise_and(img, thresh)
cv2.imshow('final',final)


cv2.waitKey(0)
cv2.destroyAllWindows()
