import json
import requests
import pyotp
from threading import Timer
import math
import pandas as pd
#import warnings
from requests.api import request
from smartapi.smartConnect import SmartConnect
from datetime import datetime, date, timedelta
import datetime, time, sys
#from warnings import filterwarnings
from nsetools import Nse
from nsepy import get_history
#filterwarnings("ignore")
userid="A114028"
apikey = "qdMI0jLV"
secretkey= "f655fc2b-fefb-4e34-b33f-aa4fc92f6a80"
password="s84jWQ"
obj=SmartConnect(api_key=apikey)
otp = "CBJQMNQKMDJUCKBZ5SEKA63CWY"
totp = pyotp.TOTP(otp)
totp = totp.now()
data = obj.generateSession(userid,password,totp)
refreshToken = data['data']['refreshToken']
flag = 0
bot_token = '2128421945:AAHz-s9UwmnCoXP4zbcQjTUm5KSS0EtHzl8'
bot_chatID = '1142557708'
# Holidays = ['2021-08-19','2021-09-10','2021-10-15','2021-11-04','2021-11-05','2021-11-19','2021-07-28']
#while datetime.time(8, 30) < datetime.datetime.now().time() < datetime.time(15, 20):
# Required credentials to interact with API
# Extracting Previous Two day's BANKNIFTY prices
nse = Nse()
symbol = 'BANKNIFTY'
today = date.today()
day = today.strftime('%A')
expiry_day = date(2021, 12, 30)
expiry_date = expiry_day.strftime("%Y-%m-%d")
print(day,"\t",datetime.datetime.now())
if (today == '2021-08-19' or today=='2021-10-15' or today=='2021-11-04' or today=='2021-11-19' or today=='2021-09-10' or today=='2021-11-05'):
    print("To day is trading holiday")
    #break
if (day == 'Sunday'):
    previousday = today - timedelta(days=3)
    print("No Trading, Today is a Holiday")
    print(previousday)
    #break
elif (day == "Saturday"):
    previousday = today - timedelta(days=2)
    print("No Trading, Today is a Holiday")
    #break
        # print(previousday)
elif (day == "Monday" or day=="Tuesday"):
    previousday = today - timedelta(days=4)
    print(previousday)
else:
    previousday = today - timedelta(days=2)
    print(previousday)

nifty_opt1 = get_history(symbol="nifty bank", start=previousday, end=today, index=True)
curr_price = obj.ltpData('NSE', symbol, 26009)['data']['ltp']

High1 = nifty_opt1.iloc[0]['High']
Low1 = nifty_opt1.iloc[0]['Low']
High2 = nifty_opt1.iloc[1]['High']
Low2 = nifty_opt1.iloc[1]['Low']


def Highest():
    if High1 > High2:
        Highest = High1
    else:
        Highest = High2
    return Highest


def Lowest():
    if Low1 < Low2:
        Lowest = Low1
    else:
        Lowest = Low2
    return Lowest

def telegram_bot_sendtext(bot_message):
    send_text= 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode = MarkdownV2&text=' +bot_message
    response = requests.get(send_text)
    return response.json()
telegram_bot_sendtext("***********BANKNIFTY***********")
telegram_bot_sendtext("Last Traded Price of Banknifty:"+str(curr_price))
telegram_bot_sendtext("Highest of Previous Two days:"+str(Highest()))
telegram_bot_sendtext("Lowest of Previous Two days:"+str(Lowest()))
