# pip install gTTS

from gtts import gTTS

### 텍스트를 음성으로 변환
text ="안녕하세요"

tts_kr = gTTS(text=text,lang='ko')
#tts_en = gTTS(text=text, lang='en')

tts_kr.save("helloKO.mp3")

f = open("helloKO.mp3",'wb')
tts_kr.write_to_fp(f)    # 한글로 한번 말하기

f.close()


### 변환된 음성을 재생
# pip install playsound
import playsound
playsound.playsound('helloKO.mp3')