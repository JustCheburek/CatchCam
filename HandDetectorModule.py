import mediapipe as mp
import math
import cv2


class HandDetector:
    """
    Finds Hands using the mediapipe library. Exports the landmarks
    in pixel format. Adds extra functionalities like finding how
    many fingers are up or the distance between two fingers. Also
    provides bounding box info of the hand found.
    """

    def __init__(self, mode=False, maxHands=2, detectionCon=0.85, minTrackCon=0.4, color_cube=(0, 0, 0),
                 color_text=(0, 0, 0)):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.minTrackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []
        self.results = ''
        self.color_cube = color_cube
        self.color_text = color_text
        self.font = cv2.FONT_HERSHEY_PLAIN

    def findHands(self, img, menu, draw=True, flipType=True, timer=3):
        """
        Finds hands in a BGR image
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {}
                # lmList
                mylmList = []
                xList = []
                yList = []
                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)

                # bbox
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), bbox[1] + (bbox[3] // 2)

                myHand["lmList"] = mylmList
                myHand["bbox"] = bbox
                myHand["center"] = (cx, cy)

                if flipType:
                    if handType.classification[0].label == "Right":
                        myHand["type"] = "Left"
                    else:
                        myHand["type"] = "Right"
                else:
                    myHand["type"] = handType.classification[0].label
                allHands.append(myHand)

                # draw
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
                    cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                                  (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                  self.color_cube, 1)
                    cv2.putText(img, f'{myHand["type"]} hand', (bbox[0] - 30, bbox[1] - 30), self.font, 1,
                                self.color_text, 1)
                    cv2.putText(img, f'Fingers up: {sum(self.fingersUp(myHand))}', (bbox[0] + 70, bbox[1] - 30),
                                self.font, 1, self.color_text, 1)
                    if menu['now'] == menu['menus'][4]:
                        if 0 < timer < 3:
                            text = f'Next move in {round(timer, 1)}'
                        else:
                            text = 'Move ready'

                        cv2.putText(img, text, (bbox[0] - 20, bbox[1] + bbox[3] + 30),
                                    self.font, 1, self.color_text, 1)

        return allHands

    def fingersUp(self, myHand, red_area_fix=40):
        """
        Finds how many fingers are open and returns in a list.
        Considers left and right hands separately
        """
        global fingers
        myHandType = myHand["type"]
        myLmList = myHand["lmList"]
        if self.results.multi_hand_landmarks:
            fingers = []
            bottom_point = myLmList[0]
            left_point = myLmList[3]
            right_point = myLmList[17]
            middle_point = myLmList[9]

            # Thumb
            if myHandType == "Right":
                if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                # разделение на верхнюю и нижнюю части
                if left_point[0] - red_area_fix <= bottom_point[0] <= right_point[0] + red_area_fix or \
                        right_point[0] - red_area_fix <= bottom_point[0] <= left_point[0] + red_area_fix:
                    # верх
                    if middle_point[1] < bottom_point[1]:
                        if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    # низ
                    else:
                        if myLmList[self.tipIds[id]][1] > myLmList[self.tipIds[id] - 2][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)

                # разделение на левую и правую части
                elif left_point[1] - red_area_fix <= bottom_point[1] <= right_point[1] + red_area_fix or \
                        right_point[1] - red_area_fix <= bottom_point[1] <= left_point[1] + red_area_fix:
                    # лево
                    if middle_point[0] < bottom_point[0]:
                        if myLmList[self.tipIds[id]][0] < myLmList[self.tipIds[id] - 2][0]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    # право
                    else:
                        if myLmList[self.tipIds[id]][0] > myLmList[self.tipIds[id] - 2][0]:
                            fingers.append(1)
                        else:
                            fingers.append(0)

        return fingers

    @staticmethod
    def findDistance(p1, p2, img=None, draw=True):
        """
        Find the distance between two landmarks based on their
        index numbers.
        """

        x1, y1 = p1
        x2, y2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, cx, cy)
        if draw:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return length, info
