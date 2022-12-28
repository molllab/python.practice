# pip install SpeechRecognition pyaudio

import speech_recognition as sr

try:
    while True:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("음성을 입력하세요.")
            audio = r.listen(source)

        try:
            stt = r.recognize_google(audio, language='ko-KR')
            print("음성변환 : ", stt)
            if "안녕" in stt:
                print("네 안녕하세요")
            elif "날씨" in stt:
                print("정말 날씨가 좋네요")
            elif "축구" in stt:
                print("월드컵 4강 진출국가는 아르헨티나 프랑스 모로코 크로아티아입니다.")

        except sr.UnknownValueError:
            print("오디오를 이해할 수 없습니다")

        except sr.RequestError as e:
            print(f"에러가 발생했습니다 : {e}")
            
except KeyboardInterrupt:
    pass