import requests
import smtplib
from alpha_vantage.timeseries import TimeSeries
from datetime import date
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()
# ---------------------Constant----------------------#
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

ALPHAVANTAGE_KEY = os.getenv("key")
ALPHAVANTAGE_URL = 'https://www.alphavantage.co/query?'

NEWS_API_KEY = os.getenv("news_key")
NEWS_API_URL = 'https://newsapi.org/v2/everything?'

SENDER = os.getenv("sender")
PASSCODE = os.getenv("pass")
RECEVER = os.getenv("rec")


# -------------------------Send email-----------------#
def getnews():
    data = [
        f"{server_news_api_endpoint.json()['articles'][i]['title']}" for i in range(3)]
    with smtplib.SMTP('smtp.gmail.com', 587, timeout=120) as conection:
        message = f"Subject:{COMPANY_NAME} stock {up_down} by {percentage}%.\n\nDear user,\n\nHeadline:\n{data[0]}\n\n{data[1]}\n\n{data[2]}\n\nYours favourite creation,\n\nBot."
        conection.starttls()
        conection.login(user=SENDER, password=PASSCODE)
        conection.sendmail(from_addr=SENDER, to_addrs=RECEVER, msg=message)
        print("message send.")


# ------------------Date-------------------#
yesterday_date = date.today() - timedelta(days=1)
day_before_yesterday_date = yesterday_date - timedelta(days=1)


# --------------------time series api----------------#
ts = TimeSeries(key=ALPHAVANTAGE_KEY, output_format='json')
raw_data, meta = ts.get_intraday(STOCK)


# -----------------Required data-------------------#
yesterday = [float(raw_data[data]['4. close'])
             for data in raw_data if data.split(' ')[0] == str(yesterday_date)]
day_before_yesterday = [float(raw_data[data]['4. close']) for data in raw_data if data.split(
    ' ')[0] == str(day_before_yesterday_date)]


# ----------------------New sending.-----------------#
NEWS_API_PARMS = {
    'q': COMPANY_NAME,
    'from': f"{yesterday_date}&to={day_before_yesterday_date}",
    'apiKey': NEWS_API_KEY,
}

server_news_api_endpoint = requests.get(
    url=NEWS_API_URL, params=NEWS_API_PARMS)


# ----------------------percentage calulation-----------------#
difference = abs(yesterday[0]-day_before_yesterday[0])
percentage = round(difference/(yesterday[0])*100)
up_down = None

# ------------------Conditional statement----------------#
if percentage >= 0:
    up_down = 'up'

else:
    up_down = 'down'
getnews()
