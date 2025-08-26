import datetime
import time

from core.Assistant import Chat_Agent
from voice.voice_engine import speak
from voice.voice_recognizer import command

def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict={
        1:"Monday",
        2:"Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
    return day_of_week
    
def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()

    if(hour>=0) and (hour<=12) and ('AM' in t):
        speak(f"Good Morning Saza, it's {day} and the time is {t}")
    elif(hour>=12) and (hour<=16) and ('PM' in t):
        speak(f"Good afternoon Saza, it's {day} and the time is {t}")
    else : 
        speak(f"Good evening Saza, it's {day} and the time is {t}")


if __name__ == "__main__":
    wishMe()
    while True:
        query = command().lower()
        if query == "none":
            continue
        # query = input ("Enter your command-> ")
        response = Chat_Agent(query)
        print("\r",end="",flush=True)
        print(f"Kylie :{response}\n")
        speak(response)
        
