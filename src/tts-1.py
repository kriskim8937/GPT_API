from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="""
스웨덴의 흥미로운 이야기를 소개할게요.

스웨덴은 역사와 문화가 풍부한 나라로, 그 중에서도 독특한 '말름뷔크'라는 작은 마을에 얽힌
 이야기가 있습니다. 이 마을은 스웨덴 남부에 위치한 아늑한 마을로, 중세 시대에 중요한 상 
업 중심지였지만, 이제는 평화로운 관광지로 변모했습니다.

옛날 옛적, 말름뷔크에는 한 사냥꾼이 살고 있었습니다. 그의 이름은 요한이었고, 그에게는 아
주 특별한 개, 루퍼스가 있었습니다. 루퍼스는 단순한 개가 아니라, 지혜롭고 예민한 본능을  
가진 동물로 알려져 있었죠.

어느 겨울, 말름뷔크에 이상한 일이 벌어졌습니다. 매일 밤마다 마을의 빵 굽는 집에서 신선한
 빵이 사라지기 시작한 것입니다. 마을 사람들은 이 사건을 신기하게 생각했지만, 누구도 범인
을 잡지 못했습니다.

그때 요한과 루퍼스가 나섰습니다. 요한은 루퍼스의 뛰어난 후각을 이용해 범인을 찾기로 결심
했습니다. 어느 날 밤, 요한과 루퍼스는 빵 굽는 집 근처에서 잠복하기로 했습니다. 밤이 깊어
지자 루퍼스가 갑자기 꼬리를 흔들며 경계했습니다. 루퍼스는 빵 굽는 집 주변을 돌며 냄새를 
맡기 시작했고, 곧이어 어두운 골목으로 뛰쳐나갔습니다.

요한은 루퍼스를 따라갔다가, 마침내 범인을 발견했습니다. 놀랍게도 그 범인은 사람도, 짐승 
도 아닌, 신비한 요정이었습니다! 이 요정은 마을 외곽의 숲에서 살며, 배가 고프면 마을에 와
서 음식을 가져가곤 했습니다. 요한은 요정을 다그치지 않고, 대신 그와 대화를 시도했습니다.
요정은 마을 사람들에게 해를 끼치려던 것이 아니라, 단지 배고픔을 달래기 위해 빵을 가져갔 
다고 설명했습니다. 요한은 마을 사람들이 이 요정을 이해하고 도와줄 것이라 확신했습니다.  
그래서 요한은 요정을 마을로 데려가 마을 사람들에게 그의 이야기를 전했습니다.

처음에는 다들 의아해했지만, 곧 요정의 진심을 이해하고 함께 지내기로 했습니다. 마을 사람 
들은 매일 아침 요정을 위해 신선한 빵과 음식을 준비해 놓았고, 요정은 이에 보답으로 마을을
 돌보며 작은 마법으로 그들을 돕기 시작했습니다.

이로써 말름뷔크는 더 따뜻하고 행복한 마을이 되었습니다. 요한과 루퍼스 덕분에, 말름뷔크는
 지금까지도 그 아름답고 신비로운 전설을 간직하고 있습니다.

이 이야기는 스웨덴의 따뜻한 마음씨와 사람들 사이의 이해와 협력을 강조하는 이야기로, 오늘
날에도 많은 이들에게 영감을 주고 있습니다.
  """,
)
response.stream_to_file(speech_file_path)

# import openai
# import pyttsx3
# import speech_recognition as sr
# from gtts import gTTS
# import os

# # Set up OpenAI GPT-3 API key
# openai.api_key = 'YOUR_OPENAI_API_KEY'

# # Initialize Text-to-Speech engine
# tts_engine = pyttsx3.init()

# # Function to get GPT-3 response
# def generate_response(prompt):
#     response = openai.Completion.create(
#         engine="text-davinci-003",  # Or the engine you’re using
#         prompt=prompt,
#         max_tokens=150
#     )
#     return response.choices[0].text.strip()

# # Function to convert text to speech
# def speak_text(text):
#     tts_engine.say(text)
#     tts_engine.runAndWait()

# # (Optional) Function to recognize speech input using microphone
# def get_speech_input():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         audio = recognizer.listen(source)
#         try:
#             text = recognizer.recognize_google(audio)
#             print(f"You said: {text}")
#             return text
#         except sr.UnknownValueError:
#             print("Sorry, I didn't catch that.")
#             return ""
#         except sr.RequestError as e:
#             print(f"Speech recognition service error: {e}")
#             return ""

# def main():
#     while True:
#         # Get user input
#         user_input = input("You: ")  # Or use get_speech_input() for voice input

#         # Generate GPT-3 response
#         response = generate_response(user_input)

#         # Print and speak the response
#         print(f"GPT-3: {response}")
#         speak_text(response)

# if __name__ == "__main__":
#     main()
