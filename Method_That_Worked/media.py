import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
import os
import numpy as np
import math

os.mkdir('finger_tip_images')#making directory for finger tip folderO
cord=[]

with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:

# Read an image, flip it around y-axis for correct handedness output (see
    # above).
    #reading image
    img1=cv2.imread("017_1.jpg")
    #resizing for convenience
    scale_percent=70
    width=int(img1.shape[1]*scale_percent/100)
    height= int(img1.shape[0]*scale_percent/100)
    dim=(width,height)

    image=cv2.resize(img1, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow("imagop",image)

    #image = cv2.flip(cv2.imread("016_.jpg"), 1)
    # Convert the BGR image to RGB before processing.
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    #Print handedness and draw hand landmarks on the image.
    print('Handedness:', results.multi_handedness)
    #print(results.multi_Handedness.classification[0].label[0])
    image_height, image_width, _ = image.shape
    annotated_image = image.copy()

    #to print the landmarks i.e x,y and z
    for hand_landmarks in results.multi_hand_landmarks:
        print('hand_landmarks:', hand_landmarks)
        print(
            f'Index finger tip coordinates: (',
            f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
            f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
            )

        #to print the points, pixel coordinates
        for point in mp_hands.HandLandmark:
            normalizedLandmark=hand_landmarks.landmark[point]
            pixelCoordinatesLandmark=mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, image_width, image_height)
            cord.append(pixelCoordinatesLandmark)
            print(point)
            print(pixelCoordinatesLandmark)
            #print(normalizedLandmark)


    mp_drawing.draw_landmarks(
          annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS,mp_drawing.DrawingSpec(color=(121,22,76),thickness=2,circle_radius=4))
    cv2.imwrite("final.png",annotated_image)
    print(cord)
    #because of the error uncallable list we have to convert cord into a list
    cord_list=[item for t in cord for item in t]
    #print(cord_list)
    #saving finger tip images into a folder
    arr=[16,24,32,40]# x cordinates of all the fingertips
    t=1# variable used for naming the finger tips
    for j in arr:
        cx=cord_list[j]
        cy=cord_list[j+1]
        a1=cx-40
        b1=cy-30
        a2=cx+90
        b2=cy+100
        palm=cv2.rectangle(image,(a1,b1),(a2,b2),(0,0,0),1)
        sliced_tip=image[b1:b2,a1:a2]
        cv2.imwrite(os.path.join('finger_tip_images','{}.jpg'.format(t)),sliced_tip)
        t+=1

    palm=cv2.rectangle(image,(a1,b1),(a2,b2),(0,0,0),1)
    #Visualize the ROI
    #cv2.imwrite("yhi.png",palm)


    #jugaad for palmprint extraction
    palm_array = np.empty((0, 2), int)
    for index, landmark in enumerate(hand_landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        if index == 0:
            palm_array = np.append(palm_array, landmark_point, axis=0)
        if index == 1:
            palm_array = np.append(palm_array, landmark_point, axis=0)
        if index == 5:
            palm_array = np.append(palm_array, landmark_point, axis=0)
        if index == 9:
            palm_array = np.append(palm_array, landmark_point, axis=0)
        if index == 13:
            palm_array = np.append(palm_array, landmark_point, axis=0)
        if index == 17:
            palm_array = np.append(palm_array, landmark_point, axis=0)

    #Finding the centroid of palmprint array
    M = cv2.moments(palm_array)
    cx, cy = 0, 0
    if M['m00'] != 0:
        pcx = int(M['m10'] / M['m00'])
        pcy = int(M['m01'] / M['m00'])
    print(pcx,pcy)
    cv2.circle(image,(pcx,pcy),5,(0,255,0),2)
    #sliced_tip=image[b1:b2,a1:a2]
    pa1=pcx-150
    pb1=pcy-150
    pa2=pcx+180
    pb2=pcy+150
    palm=cv2.rectangle(image,(pa1,pb1),(pa2,pb2),(0,0,0),1)
    sliced_palm=image[pb1:pb2,pa1:pa2]
    #sliced_palm=image[cord_list[11]:cord_list[1]+100,cord_list[10]:cord_list[0]+100]
    #cv2.imwrite("sliced.png",sliced_tip)#if you want a single tip as output

    #Palmrint Output
    cv2.imwrite("slicedpalm.png",sliced_palm)


    #Now lets do some code for getting hand-geometry that is-
    #list to contian all values
    Hand_geo=[]
    #Thumb length(TL)
    TLX1=cord_list[2]
    TLY1=cord_list[3]
    TLX2=cord_list[8]
    TLY2=cord_list[9]
    TLp1=[TLX1,TLY1]
    TLp2=[TLX2,TLY2]
    TL=math.sqrt(((TLp1[0]-TLp2[0])**2)+((TLp1[1]-TLp2[1])**2))
    Hand_geo.append(TL)
    #print(TL)

    #Index finger length(IFl)
    IFLX1=cord_list[10]
    IFLY1=cord_list[11]
    IFLX2=cord_list[16]
    IFLY2=cord_list[17]
    IFLp1=[IFLX1,IFLY1]
    IFLp2=[IFLX2,IFLY2]
    IFL=math.sqrt(((IFLp1[0]-IFLp2[0])**2)+((IFLp1[1]-IFLp2[1])**2))
    Hand_geo.append(IFL)
    #print(IFL)

    #Middle finger lenth(MFL)
    MFLX1=cord_list[18]
    MFLY1=cord_list[19]
    MFLX2=cord_list[24]
    MFLY2=cord_list[25]
    MFLp1=[MFLX1,MFLY1]
    MFLp2=[MFLX2,MFLY2]
    MFL=math.sqrt(((MFLp1[0]-MFLp2[0])**2)+((MFLp1[1]-MFLp2[1])**2))
    Hand_geo.append(MFL)
    #print(MFL)
    #Ring finger length(RFL)
    RFLX1=cord_list[26]
    RFLY1=cord_list[27]
    RFLX2=cord_list[16]
    RFLY2=cord_list[17]
    RFLp1=[RFLX1,RFLY1]
    RFLp2=[RFLX2,RFLY2]
    RFL=math.sqrt(((RFLp1[0]-RFLp2[0])**2)+((RFLp1[1]-RFLp2[1])**2))
    Hand_geo.append(RFL)
    #print(RFL)
    #Pinky finger length(PFL)
    PFLX1=cord_list[34]
    PFLY1=cord_list[35]
    PFLX2=cord_list[40]
    PFLY2=cord_list[41]
    PFLp1=[PFLX1,PFLY1]
    PFLp2=[PFLX2,PFLY2]
    PFL=math.sqrt(((PFLp1[0]-PFLp2[0])**2)+((PFLp1[1]-PFLp2[1])**2))
    Hand_geo.append(PFL)
    #print(PFL)
    #Palm Width(PW)
    PWX1=cord_list[10]
    PWY1=cord_list[11]
    PWX2=cord_list[34]
    PWY2=cord_list[35]
    PWp1=[PWX1,PWY1]
    PWp2=[PWX2,PWY2]
    PW=math.sqrt(((PWp1[0]-PWp2[0])**2)+((PWp1[1]-PWp2[1])**2))
    Hand_geo.append(PW)
    #print(PW)

    #Knuckle Length->
    #Thumb-Index(TI)
    TIp1=[TLX1,TLY1]
    TIp2=[IFLX2,IFLY2]
    Thumb_Index=math.sqrt(((TIp1[0]-TIp2[0])**2)+((TIp1[1]-TIp2[1])**2))
    Hand_geo.append(Thumb_Index)
    #print(Thumb_Index)
    #Index-Middle(IM)
    IMp1=[IFLX1,IFLY1]
    IMp2=[MFLX2,MFLY2]
    Index_Middle=math.sqrt(((IMp1[0]-IMp2[0])**2)+((IMp1[1]-IMp2[1])**2))
    Hand_geo.append(Index_Middle)
    #print(Index_Middle)
    #Middle-Ring(MR)
    MRp1=[MFLX1,MFLY1]
    MRp2=[RFLX2,RFLY2]
    Middle_Ring=math.sqrt(((MRp1[0]-MRp2[0])**2)+((MRp1[1]-MRp2[1])**2))
    Hand_geo.append(Middle_Ring)
    #print(Middle_Ring)
    #Ring-Pinky(RP)
    RPp1=[RFLX1,RFLY1]
    RPp2=[PFLX2,PFLY2]
    Ring_Pinky=math.sqrt(((RPp1[0]-RPp2[0])**2)+((RPp1[1]-RPp2[1])**2))
    Hand_geo.append(Ring_Pinky)
    #print(Ring_Pinky)
    print(Hand_geo)

#Printing the list containing all the hand geometry values
