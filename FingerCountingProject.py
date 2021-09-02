import cv2
import time
import os
import hand as htm

wCam, hCam = 640, 480  # weight==3,height==4

cap = cv2.VideoCapture(0)  # for open cam

cap.set(3, wCam)  # resize the window
cap.set(4, hCam)

# stored image

folderPath = "fingers"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for i in myList:
    image = cv2.imread(f'{folderPath}/{i}')
    overlayList.append(image)  # path of every image in list
# fps
pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()  # read image
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []
        # Thumb
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        totalFingers=sum(fingers)
        img[0:200, 0:200] = overlayList[totalFingers] #Change image of fingers
        cv2.rectangle(img,(20,255),(170,425),(0,255,0),cv2.FILLED)
        cv2.putText(img,f'{totalFingers}',(45,375),cv2.FONT_ITALIC,5,(255,0,0),25)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'fps:{int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)

    cv2.imshow("test", img)  # show image
    cv2.waitKey(1)
