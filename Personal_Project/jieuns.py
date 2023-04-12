import urllib.request
import requests
from bs4 import BeautifulSoup
import json
import datetime
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pyaudio
import speech_recognition as sr
from gtts import gTTS
import playsound
import os
from konlpy.tag import Komoran
import random

def nlp_text(text):
    komoran = Komoran()
    nouns = komoran.nouns(text)
    
    return nouns
    
def speak(text):
    tts = gTTS(text=text, lang="ko")
    filename="voice.mp3"
    try:
        tts.save(filename)
        playsound.playsound(filename)
        os.remove("voice.mp3")
    except:
        os.remove("voice.mp3")
        tts = gTTS(text=text, lang="ko")
        filename="voice.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove("voice.mp3")

def recognizer_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("'recognizer' must be 'Recognizer' instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("'microphone' must be 'Microphone' instance")
        
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        speech = recognizer.listen(source)
    
    try :
        wording = recognizer.recognize_google(speech, language="ko-KR")
        
    except:
        pass
    
    return wording

def crawling(url):
    
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, "html.parser")
    
    return soup

def weather_info(text):
    texts = nlp_text(text)
    text = ' '.join(texts)
    try:
        url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query={text}"
        soup = crawling(url)

        section = soup.find("section", {"class":"sc_new cs_weather_new _cs_weather"})

        loction = section.find("h2", {"class":"title"}).get_text().strip()
        temp = section.find("div", {"class":"temperature_text"}).get_text().strip()
        weather = section.find("div", {"class":"weather_main"}).get_text().strip()
        min_max_temp = section.find("div", {"class":"cell_temperature"}).get_text().strip()
        info_temp = section.find("div", {"class":"temperature_info"}).get_text().strip()
        fi_dust = section.find("li", {"class":"item_today level1"}).get_text().strip()
        ul_dust = section.find("li", {"class":"item_today level2"}).get_text().strip()
        rain_rate = section.find("div", {"class":"cell_weather"}).get_text().strip()

        answer = f"{loction} 의 기온은 {temp} 날씨는 {weather} 에요. 오늘 {min_max_temp} 에요. {info_temp} {fi_dust} 이고 {ul_dust} 에요. 강수률은 {rain_rate} 에요."

    except:
        pass

    return answer


def lotto_info(text):
    try:
        url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query={text}"
        soup = crawling(url)

        turn = soup.find("div", {"class":"select_tab"}).get_text().split(" ")
        turn = [x for x in turn if x.strip()]
        lotto = soup.find("div", {"class":"win_number_box"}).get_text().split(" ")
        lotto = [x for x in lotto if x.strip()]
        answer = f"{turn[0]} 1등 당첨 번호는 {', '.join(lotto[:6]) } 이고 보너스 볼은 {lotto[6]} 입니다. 1등 당첨금은 {lotto[9][:-1]}원 입니다."

    except:
        pass

    return answer


def horoscope_info(): # 운세
    try:
        url = 'https://m.search.naver.com/p/csearch/dcontent/external_api/json_todayunse_v2.naver'
        headers = {'user-agent': 'Mozilla/5.0'}

        params = {
            '_callback': 'window.__jindo2_callback._fortune_my_0',
            'gender': '',                # 유저 정보
            'birth': '',
            'solarCal': 'solar',
            'time': '',
        }

        response = requests.get(url, params=params, headers=headers).text
        response = BeautifulSoup(response, 'html.parser').text

        soup = response.replace("window.__jindo2_callback._fortune_my_0(", "")[:-2]
        soup = soup.replace("\n", "")
        soup = soup.replace("\t", "")
        soup = soup[soup.find("content : [") : soup.find("]")+1]
        soup = soup[soup.find("{") : soup.rfind("}")+1]
        keyword = soup[soup.find('"keyword" : "')+13 : soup.find('", "desc"')]

        answer = f"{keyword}"
    
    except:
        pass
    
    return answer


def restaurant_info(text):
    texts = nlp_text(text)
    text = ' '.join(texts)
    try:
        url = f"https://map.naver.com/v5/api/search?caller=pcweb&query={text}"
        response = requests.get(url)
        jsonObject = json.loads(response.text)['result']
    
        search_query = jsonObject['metaInfo']['searchedQuery']
        search_list = jsonObject['place']['list']
        search_info = []
        for i in search_list:
            temp = []
            temp.append(i['name'])
            temp.append(i['category'])
            temp.append(i['context'])
            temp.append(i['address'])
            temp.append(i['tel'])
            temp.append(i['bizhourInfo'])
            temp.append(i['menuInfo'])
    
            search_info.append(temp)
    
        answer = f"{search_query} 의 맛집 리스트는 {', '.join([i[0] + ' ' + ' '.join(i[1]) for i in search_info])}이 있습니다."
        
    except:
        pass
    
    return answer


def hot_news_info():
    try :
        url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1="
        soup = crawling(url)
    
        ul = soup.find("ul", {"class":"section_list_ranking_press _rankingList"})
        a_tag = ul.findAll("a", {"class":"list_tit nclicks('rig.renws2')"})
        title = []
        for i, a_tag in enumerate(a_tag):
            title.append(f"{i+1} 번 뉴스 {a_tag.get_text()}")

        answer = f"실시간 뉴스 {''.join(title)}"
    
    except:
        pass
    
    return answer
    
    
def news_info(text):
    texts = nlp_text(text)
    for text in texts:
        try:
            param = {
                "정치" : ["100", "cluster_text_headline nclicks(cls_pol.clsart)"],
                "경제" : ["101", "cluster_text_headline nclicks(cls_eco.clsart)"],
                "사회" : ["102", "cluster_text_headline nclicks(cls_nav.clsart)"],
                "생활문화" : ["103", "cluster_text_headline nclicks(cls_lif.clsart)"],
                "세계" : ["104", "cluster_text_headline nclicks(cls_lif.clsart)"],
                "IT과학" : ["105", "cluster_text_headline nclicks(cls_sci.clsart)"]
            }
            url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1="    
            soup = crawling(url+param[text][0])
    
            td = soup.find("td", {"class":"content"})
            a_tag = td.findAll("a", {"class":param[text][1]})
            title = []
            try:
                for i, a_tag in enumerate(a_tag):
                    title.append(f"{i+1} 번 뉴스 {a_tag.get_text()} ")
            except:
                pass
    
            answer = f"{text} 뉴스 {''.join(title)}"
            
        except:
            pass
    
    return answer


def find_stock_code(text):
    try:
        url = f"https://ac.finance.naver.com/ac?_callback=window.__jindo2_callback._$3361_0&q={text}&q_enc=euc-kr&st=111&frm=stock&r_format=json&r_enc=euc-kr&r_unicode=0&t_koreng=1&r_lt=111"
        response = requests.get(url).text
    
        soup = response.replace("window.__jindo2_callback._$3361_0(", "")[:-1]
        soup = soup.replace("\n", "")
        soup = soup.replace("\t", "")
        code = soup[soup.find('"items" : [[[["')+15 : soup.find('"],["')]
    
    except:
        pass

    return code


def stock_info(text):
    if text.find("주가") != -1 :
        text = text[:text.find("주가")].strip()
    elif text.find("주식") != -1 :
        text = text[:text.find("주식")].strip()
        
    try:
        code = find_stock_code(text)
        url = f"https://polling.finance.naver.com/api/realtime?query=SERVICE_ITEM:{code}"
        response = requests.get(url)
        jsonObject = json.loads(response.text)['result']['areas']
    
        data = []
        for i in jsonObject:
            if i['datas'][0]['rf'] == "2" :     #상승
                data.append(i['datas'][0]['nm'])
                data.append(i['datas'][0]['nv']) #주가
                data.append(i['datas'][0]['cv']) #전일대비상승금액
                data.append(i['datas'][0]['cr']) #전일대비상승률
                    
                answer = f"{data[0]} 의 주가는 {data[1]} 원 입니다. 전일대비 {data[2]} 원 상승, {data[3]}% 상승 입니다."
                    
            elif i['datas'][0]['rf'] == "5" :   #하락
                data.append(i['datas'][0]['nm'])
                data.append(i['datas'][0]['nv']) #주가
                data.append(i['datas'][0]['cv']) #전일대비상승금액
                data.append(i['datas'][0]['cr']) #전일대비상승률
                    
                answer = f"{data[0]} 의 주가는 {data[1]} 원 입니다. 전일대비 {data[2]} 원 하락, {data[3]}% 하락 입니다."
                
            else:
                answer = f"{data[0]} 의 주가는 {data[1]} 원 입니다. 전일대비 {data[2]} 원, {data[3]}% 입니다."
        
    except:
        answer = "알 수 없는 정보입니다. 다시 말해주세요."
        pass
        
    return answer

def get_time():
    now = datetime.datetime.now()
    answer = f"현재 시각은 {now.hour}시 {now.minute}분 입니다."
    
    return answer

def schedule_list(text):
    try :
        today = datetime.datetime.now()
        time = datetime.datetime.now().time()

        schedule = []
        if text.find("추가") != -1:

            date = text[:text.find("일")+1] + " " + str(time.replace(hour=0, minute=0, second=0, microsecond=0))
            date = datetime.datetime.strptime(date, "%m월 %d일 %H:%M:%S")
            date = str(date)[5:10]

            event = text[text.find("일")+1:text.find("추가")].strip()

            with open("schedule.txt", "a") as f:
                f.write(f"{date} {event}\n")

            answer = "일정이 정상적으로 추가 되었습니다."

        elif text.find("보여") != -1 or text.find("알려") != -1:
            with open("schedule.txt", "r") as f:
                schedule = f.readlines()

            if schedule == []:
                answer = "스케줄이 없습니다."
            
            elif text.find("전체") != -1:
                answer = "전체 일정 "
                for i in schedule:
                    date = i[:5].strip()
                    date = datetime.datetime.strptime(date, "%m-%d")
                    date = date.strftime("%m월 %d일")
                    event = i[5:]
                                        
                    answer += (date + event)

            else :
                temp = []
                for i in schedule:
                    if i.find(str(today)[5:10]) != -1:
                        answer = ""
                        date = i[:5].strip()
                        date = datetime.datetime.strptime(date, "%m-%d")
                        date = date.strftime("%m월 %d일")
                        event = i[5:]
                                            
                        temp.append(date + event)
                
                if temp == []:
                    answer = "오늘 일정이 없습니다."
                
                else :
                    answer = "오늘 일정은 " + "".join(temp) + "입니다."

        else :
            answer = "알 수 없는 정보입니다. 다시 말씀해주세요."
    
    except:
        answer = "알 수 없는 정보 입니다. 다시 말씀해주세요."
        pass
    
    return answer

def log(text):
    time = datetime.datetime.now()
    font_path = 'C:/Windows/Fonts/malgun.ttf'
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rcParams['font.family'] = font_name
    
    if text.find("관리자") != -1:
        content = []

        with open("log.txt", "r", encoding = "UTF-8") as f:
            content_line = f.readlines()
            
        for i in content_line:
            nouns = nlp_text(i[10:].strip())
            for noun in nouns:
                content.append(noun)
                
        content = " ".join(content)

        word_count = Counter(content.split())
        word_count = sorted(word_count.items(), key=lambda x : x[1], reverse=True)
        
        words = [x[0] for x in word_count]
        counts = [x[1] for x in word_count]
        
        plt.bar(words, counts)
        plt.title("사용 데이터")
        plt.xlabel("Words")
        plt.ylabel("Counts")
        plt.xticks(rotation = 45)
        plt.show()

    else:
        try:
            with open("log.txt", "a") as f:
                f.write(f"{time} {text}\n")
                
        except:
            with open("log.txt", "w") as f:
                f.write(f"{time} {text}\n")
                

if __name__ == "__main__":
    
    run = True
    cnt = 0
    
    while run:    
        recognizer = sr.Recognizer()
        mic = sr.Microphone(device_index=1)
        
        print("지금 말해주세요.")
        wording = recognizer_mic(recognizer, mic)
        print(wording)
        
        try:
            if "지은스" in wording or "지은" in wording or "지은아" in wording or "지은쓰" in wording:
                ye = random.choice(["응?", "넹?", "넵?", "네네", "저를 부르셨나요"])
                speak(ye)
            
            if "날씨" in wording:
                speak(weather_info("날씨"))
                log(wording)
                break
            
            if "로또" in wording:
                speak(lotto_info("로또"))
                log(wording)
                break
                
            if "운세" in wording:
                speak(horoscope_info())
                log(wording)
                break
            
            if "음식" in wording or "맛집" in wording:
                speak(restaurant_info(wording))
                log(wording)
                break
            
            if "정치" in wording or "정치" in wording or "경제" in wording or "사회" in wording or "문화" in wording or "세계" in wording or "과학" in wording:
                speak(news_info(wording))
                log(wording)
                break
            elif "뉴스" in wording:
                speak(hot_news_info())
                log(wording)
                break
                
            if "주식" in wording or "주가" in wording:
                speak(stock_info(wording))
                log(wording)
                break
            
            if "시간" in wording or "시각" in wording:
                speak(get_time())
                log(wording)
                break
            
            if "일정" in wording or "스케줄" in wording:
                speak(schedule_list(wording))
                log(wording)
                break
            
            if "관리자" in wording:
                log(wording)
                break
                
            if "종료" in wording:
                speak("뾰로롱")
                run = False
                break
            
        except:
            if cnt < 5:
                cnt += 1
                continue
            else:
                run = False
                break
