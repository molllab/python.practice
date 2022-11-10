# pip install opencv-python
# pip install pyautogui

import time
import pyautogui

##### pyautogui의 키 표기 알고싶을 때
# print(pyautogui.KEYBOARD_KEYS)

#---------------------------------------------------------------------------

##### 엔터 반복적으로 칠 일이 있어서 만들어 봄
for _ in range(1000):
    pyautogui.press(['up','end','down','enter'])
    # time.sleep(0.2)
    
#---------------------------------------------------------------------------

##### 교육듣는데 새로고침 자동으로 누르려고
# 화면에 이미지와 동일한게 나타나면, 그 위치로 이동해서 클릭하는 예제입니다.
# 버튼 등을 자동으로 클릭하게 만들고 싶은 경우에 사용할 수 있습니다.

# 사용자가 정지시키기 전까지 무한히 반복
while True:
    # locateCenterOnScreen 함수는 button_image.png 사진과 동일한 것이 화면에 등장하면 그 중심 좌표를 알려줍니다.
    # 없으면 None을 반환합니다.
    point = pyautogui.locateCenterOnScreen('refresh.png')

    # point가 None이 아니면 코드를 실행합니다.
    # (None이 아니다 = button_image.png 이미지를 화면에서 찾았다.)
    if point != None:
        # point 안에는 좌표(x, y)가 들어있습니다
        # 그 좌표를 찾아가 클릭합니다.
        pyautogui.click(point.x, point.y)

    # 프로그램이 5초 동안 대기합니다.
    time.sleep(5)