# pip install opencv-python mediapipe
import cv2
import mediapipe as mp
import math

# 제스쳐 정보 세팅
if True:
    from itertools import permutations

    # 손가락 개수 세팅
    # 리스트 맨 앞부터 [ 엄지, 검지, 중지, 약지, 새끼 ]
    data = {
        "Zero" : [ False, False, False, False, False],
        "One" : [ True, False, False, False, False ],
        "Two" : [ True, True, False, False, False ],
        "Three" : [ True, True, True, False, False ],
        "Four" : [ True, True, True, True, False ],
        "Five" : [ True, True, True, True, True ]
    }

    # 손가락 핀 개수별로 모든 제스쳐 조합 만들기
    # ex) 엄지를 하나펴도 하나고, 검지를 하나 펴도 하나
    gesture = []

    for k, v in data.items():
        for item in set(permutations(v, 5)):
            gesture.append(list(item))
            gesture[-1].append(k)

else:
    # 원래 예제에 있는 것
    gesture = [
        [True, True, True, True, True, "Hi!"],
        [False, True, True, False, False, "Yeah!"],
        [True, True, False, False, True, "SpiderMan!"]
        ]

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

            for i in range(0, len(gesture)):
                flag = True
                for j in range(0,5):
                    if(gesture[i][j] != open[j]):
                        flag = False

                if flag ==True:
                    # gesture[i][5]는 'one', 'two', ... 'five'
                    cv2.putText(img, gesture[i][5], (round(text_x) - 50, round(text_y) - 250), cv2.FONT_HERSHEY_PLAIN, 4, (0,0,0), 4)
                    # 처리
                    if user_function:
                        user_function(gesture[i][5])

            mpDraw.draw_landmarks (img, handLms, mpHands. HAND_CONNECTIONS)

def test_function(finger_info):
    #####################################################################
    # 여기서 여러분이 새롬게 만들고 싶은 기능을 구현하면 됩니다.
    # ex) 점수를 구글 스프레드시트로 전달한다던지(지하식당 별점)
    #     전등, 음악 등을 키고 끄는 것
    #####################################################################
    # print(finger_info)
    pass

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
        check_finger(res, test_function)

        cv2.imshow("HandTracking", img)
        cv2.waitKey(1)