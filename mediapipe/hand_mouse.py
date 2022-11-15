# pip install opencv-python mediapipe
import cv2
import mediapipe as mp
import math
import pyautogui

open = [False, False, False, False, False]
items = [True, True, False, False, False]

# 미디어파이프
mpHands=mp.solutions.hands
my_hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

max_thumb_dist = -1

compareIndex = [[None, None],[6,8],[10, 12],[14,16], [18,20]]
def dist(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2,2)) + math.sqrt(math.pow(y1 - y2,2))
# 미디어파이프 손가락 마디정보 분석하는 함수
# user_function에 함수명을 전달하면 그 함수를 실행해 줌
def check_finger(results, user_function=None):
    global max_thumb_dist
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            ### 손 모양 hold 인식
            for i in range(0,5):
                # Hand index 거리 : 0번에서 n번까지 거리
                if i == 0:
                    # 엄지일 때만 다른 기준
                    # 0~4 까지 길이
                    cur_dist_thumb = dist(handLms.landmark[0].x, handLms.landmark[0].y, handLms.landmark[4].x, handLms.landmark[4].y)
                    open[i] = cur_dist_thumb >= max_thumb_dist * 0.8 
                    if max_thumb_dist < cur_dist_thumb:
                        max_thumb_dist = cur_dist_thumb
                else:
                    dist_1 = dist(handLms.landmark[0].x, handLms.landmark[0].y, handLms.landmark[compareIndex[i][0]].x, handLms.landmark[compareIndex[i][0]].y)
                    dist_2 = dist(handLms.landmark[0].x, handLms.landmark[0].y, handLms.landmark[compareIndex[i][1]].x, handLms.landmark[compareIndex[i][1]].y)
                    open[i] = dist_1 < dist_2
            text_x = (handLms.landmark[0].x * w)
            text_y = (handLms.landmark[0].y * h)

            gesture_0 = [False, False, False, False, False]
            flag = True
            for j in range(0,5):
                if(gesture_0[j] != open[j]):
                    flag = False

            if flag == True:
                cv2.putText(img, "hold", (round(text_x) - 50, round(text_y) - 250), cv2.FONT_HERSHEY_PLAIN, 4, (0,0,0), 4)
                # 처리
                if user_function:
                    user_function("hold")

            else:
                # 홀드 아닌경우 0번과 검지(8)의 좌표를 비교해서 방향 체크
                x0 = handLms.landmark[0].x
                y0 = handLms.landmark[0].y
                x8 = handLms.landmark[8].x
                y8 = handLms.landmark[8].y

                offset = 20

                # 좌
                if x8 > x0 and (abs(y8 - y0) < 0.2):
                    pyautogui.move(-offset, 0)
                    print("left %.2f" % x0, ",", "%.2f" % y0, "==>", "%.2f" % x8, ",", "%.2f" % y8)
                # elif x8 > x0 and y8 > y0:
                #     pyautogui.move(-offset, offset)
                # elif x8 > x0 and y8 < y0:
                #     pyautogui.move(-offset, -offset)

                # 우
                # elif x8 < x0 and y8 > y0:
                #     pyautogui.move(offset, offset)
                elif x8 < x0 and (abs(y8 - y0) < 0.2):
                    pyautogui.move(offset, 0)
                    print("right %.2f" % x0, ",", "%.2f" % y0, "==>", "%.2f" % x8, ",", "%.2f" % y8)
                # elif x8 < x0 and y8 < y0:
                #     pyautogui.move(offset, -offset)

                # 상
                elif (abs(x8 - x0) < 0.2) and y8 < y0:
                    pyautogui.move(0, -offset)
                    print("up %.2f" % x0, ",", "%.2f" % y0, "==>", "%.2f" % x8, ",", "%.2f" % y8)

                # 하
                elif (abs(x8 - x0) < 0.2) and y8 > y0:
                    pyautogui.move(0, offset)
                    print("down %.2f" % x0, ",", "%.2f" % y0, "==>", "%.2f" % x8, ",", "%.2f" % y8)

            mpDraw.draw_landmarks (img, handLms, mpHands. HAND_CONNECTIONS)

if __name__ == '__main__':
    cap = cv2.VideoCapture (0)
    while True:
        # 카메라 이미지 캡쳐
        success, img = cap.read()
        h,w,c = img.shape
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # 이미지를 분석(손가락 마디 등)
        res = my_hands.process(imgRGB)

        # 손가락 개수
        check_finger(res)

        #cv2.imshow("HandTracking", img)
        cv2.waitKey(1)