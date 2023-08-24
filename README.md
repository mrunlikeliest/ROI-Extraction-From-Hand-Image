# ROI-Extraction-From-Hand-Image
#### Submitted by: Shubham Santosh Upadhyay<br>
#### Guided by: Asst. Prof. Rahul Chatterjee (UW Madison)<br>
-----------------------------------------------------------------------------------------

# Required Libraries:
1. OpenCV
2. Numpy
3. MediaPipe
-----------------------------------------------------------------------------------------

# Abstract:<br>
As we all know biometric authentication plays an important role in ensuring security and extraction of biometric features is always a challenge. We have separate datasets available for separate biometrics but an attempt is being made to extract all three biometrics i.e. fingertip, Palmprint, and Hand-geometry from a single hand image. We have tried different methods and finally found the most apt solution. A significant amount of time is spent on surveying different research papers on "Authentication with the help of different biometrics" and collecting all possible datasets.

------------------------------------------------------------------------------------------
# Datasets that can be used for further research works:<br>

[Palmprint Dataset-Hindawi](https://staffusm-my.sharepoint.com/personal/shahrel_usm_my/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fshahrel%5Fusm%5Fmy%2FDocuments%2FResearch%5FData%2FIBGHT%5FGroundtruth&originalPath=aHR0cHM6Ly9zdGFmZnVzbS1teS5zaGFyZXBvaW50LmNvbS86ZjovZy9wZXJzb25hbC9zaGFocmVsX3VzbV9teS9FbF9kblQ5bmF1QlBwQS0yYmdWT2ZMMEJxLVNUcWg2V2k0M2M1eFZKVl9ZR2x3P3J0aW1lPXNlZ0FHUDhhMlVn)

[GPDS Dataset](https://gpds.ulpgc.es/)

[11k Hands](https://sites.google.com/view/11khands)

[IITD Dataset](https://www4.comp.polyu.edu.hk/~csajaykr/IITD/Database_Palm.htm)

[Boston University Hand Login Dataset](http://vip.bu.edu/projects/hcis/hand-login/dataset/)

[Fingerprint and Iris Databases](https://www.neurotechnology.com/download.html)

[University of Notre Dame Iris Dataset](https://cvrl.nd.edu/projects/data/)

[CASIA](http://www.cbsr.ia.ac.cn/IrisDatabase.htm)

[XM2VTSDB multi-modal face database](http://www.ee.surrey.ac.uk/CVSSP/xm2vtsdb/)

**Some sites give you datasets directly, on others you have to request.

------------------------------------------------------------------------------------------

## Methods that didn't work:
1. Skin Segmentation->Contour detection->Finding min area contour to find fingerprint.
2. Skin Segmentation->Finding Convex hull and Contour intersection point and finally locating ROI
3. Using deep learning (limited computational power)
4. Extracting ROIs using Haar Cascade.
 
Codes can be found in the Methods_That_Didnt_Work folder.

------------------------------------------------------------------------------------------

## Method That worked:
1. Using [Mediapipe Hands](https://google.github.io/mediapipe/solutions/hands.html) opensource framework.

------------------------------------------------------------------------------------------

# Methodology:

1. MediaPipe Hands is a high-fidelity hand and finger tracking solution. It employs machine learning (ML) to infer 21 3D landmarks of a hand from just a single frame.
2. We used media pipe as it solves the problem of contour detection, skin segmentation, background removal, and dynamics.
3. The hand landmarks are found and then normalized to get the coordinates of 21 points on the hand.

   <img src="images/hand.PNG" height="200" width="500">
4. These coordinates are used to draw ROIs.For example- points 8,12,16 and 20 represent the index, middle, ring, and pinky finger respectively. The thumb is not considered as it is tilted during photo capture.
5. Palmprint is captured by storing and finding the centroid of all the palm boundary points (0,1,5,9,13,17).
6. Hand geometry includes Length of all fingers, palm width, and distance between knuckles.

------------------------------------------------------------------------------------------

# Input:<br>
Input image<br>
 <Img src="images/017_1.JPG" height="200" width="300"><br>
------------------------------------------------------------------------------------------
 
# Output:<br>
 Hand Landmarks:<br>                                
 <img src="images/final.png" height="200" width="300">  <br> 
 Finger Tips:<br>
 <img src="images/1.jpg" height="100" width="100"> <img src="images/2.jpg" height="100" width="100"> <img src="images/3.jpg" height="100" width="100"> <img src="images/4.jpg" height="100" width="100"> <br>
 Palmprint:<br>
 <img src="images/slicedpalm.png" height="200" width="300"><br>
 Hand Geometry Values:<br>
 <img src="images/Hand_Geo_Values.PNG" height="60" width="900"><br>
 
 ------------------------------------------------------------------------------------------
 
 # Future Work:<br>
 Furthermore, this work can be used to extract features and use them for authentication.<br>
 
 For fingerprint feature extraction from a low-resolution image (The image obtained from the dataset was not meant for fingerprints and hence it is a big problem to extract fingerprint features):<br>
 1. For preprocessing, as the pic has almost no fingerprint it needed to be preprocessed a lot.<br>
    <https://answers.opencv.org/question/6364/fingerprint-matching-in-mobile-devices-android-platform/><br>
 2. For fingerprint Matching.<br>
    <https://github.com/Utkarsh-Deshmukh/Fingerprint-Feature-Extraction><br>

 For palmprint feature extraction.<br>
    <https://github.com/AdrianUng/palmprint-feature-extraction-techniques><br>
 
 -------------------------------------------------------------------------------------------
 # References:<br>
     [1]. <https://docs.google.com/spreadsheets/d/1WyfpljI49AqvCO_lV3-XOfHVg4Ilks_yJGWhZXCLU_M/edit?usp=sharing>
 
 

   

