import requests
adressHd = "https://dt.miet.ru/ppo_it/api/hum/"
T = 0
H = 0
Hd = 0
head={"X-Auth-Token": "ciTw9o"}
def TempFromTH(a):
    adressTH = "https://dt.miet.ru/ppo_it/api/temp_hum/"
    rew = requests.get(adressTH + str(a))
    Temperature = rew.json()["temperature"]
    return Temperature
def HumidityFromTH(a):
    adressTH = "https://dt.miet.ru/ppo_it/api/temp_hum/"
    rew = requests.get(adressTH + str(a))
    Humidity = rew.json()["humidity"]
    return Humidity
def Hd(a):
    adressTH = "https://dt.miet.ru/ppo_it/api/temp_hum/"
    rew = requests.get(adressHd + str(a))
    humidityd = rew.json()["humidity"]
    return humidityd
def TempA():
    f = 0
    for i in range(1,5):
        f = f + TempFromTH(i)
    f = f/4
    return f
def HumidityA():
    f = 0
    for i in range(1,5):
        f = f + HumidityFromTH(i)
    f = f/4
    return f
def HdA():
    f = 0
    for i in range(1,7):
        f = f + Hd(i)
    f = f/4
    return f
def OpenFort(a):
    rew = requests.patch("https://dt.miet.ru/ppo_it/api/fork_drive", params = {"state":str(a)}, headers = head)
def Watering(a,b):
    rew = requests.patch("https://dt.miet.ru/ppo_it/api/watering", params = {"id":str(b), "state" : str(a)}, headers = head)
def totalHum(a):
    rew = requests.patch("https://dt.miet.ru/ppo_it/api/total_hum", params = {"state" : str(a)}, headers = head)
