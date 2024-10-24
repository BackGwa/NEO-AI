import requests, vlc, yt_dlp, time
from datetime import datetime
from threading import Thread
from .IOEngine import IOEngine
from .MessageEngine import MessageEngine

class InterpretEngine:
    def __init__(self, io_manager: IOEngine, message_manger: MessageEngine, button_pin: int, openweather_api: str):
        self.message_manger = message_manger
        self.openweather_api = openweather_api

        io_manager.register_input(button_pin, self.__stop_music__)

    def timer(self, second: int) -> str:
        if second > 60:
            text = f"{second // 60}분 "
            if int(second % 60) != 0:
                text += f"{int(second % 60)}초"
        else:
            text = f"{second}초"
        T = Thread(target=self.__alloc_timer__, args=(second,))
        T.start()
        return f"{text} 타이머를 시작할게요."

    def __alloc_timer__(self, second: int) -> str:
        time.sleep(second + 1)
        player = vlc.MediaPlayer("res/ringing.mp3")
        player.play()

    def date(self) -> str:
        current_datetime = datetime.now()
        return f"오늘은 {current_datetime.strftime('%Y 년 %m 월 %d 일')}이에요."

    def clock(self) -> str:
        current_datetime = datetime.now()
        return f"지금은 {current_datetime.strftime('%H 시 %M 분')}이에요."
    
    def weather(self):
        location_response = requests.get("http://ip-api.com/json/")
        location_data = location_response.json()
        
        if location_data['status'] != 'success':
            return "위치 정보를 가져오는 데 실패했어요."

        latitude = location_data['lat']
        longitude = location_data['lon']
        city = location_data['city']

        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={self.openweather_api}&units=metric&lang=kr"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if weather_data.get('cod') != 200:
            return "날씨 정보를 가져오는 데 실패했어요."

        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        
        return f"현재 {city}의 날씨는 {description}이며, 섭씨 {round(temperature, 1)}도 이에요."

    def music(self, name: str):
        T = Thread(target=self.__play_music__, args=(name,))
        T.start()
        return f"{name}을 재생할게요, 버튼을 눌러 종료할 수 있어요."
    
    def __parsing_url__(self, query: str):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
                return info['url']
        except Exception as e:
            return None

    def __play_music__(self, name: str):
        url = self.__parsing_url__(name)
        self.player = vlc.MediaPlayer(url)
        time.sleep(1)
        self.player.play()

    def __stop_music__(self):
        self.player.stop()

    def send_message(self, to: str, message: str):
        return self.message_manger.raw_message(to, { "content" : message })