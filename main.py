import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
URL = "https://www.amazon.com/Instant-Pot-Pressure-Steamer-Sterilizer/dp/B08PQ2KWHS/ref=dp_fod_2?pd_rd_i=B08PPZWNCV" \
      "&th=1 "
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/84.0.4147.125 Safari/537.36", 
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}
TARGET_PRICE = 120
EMAIL_ENDPOINT = "smtp.gmail.com"
EMAIL = os.environ['EMAIL']

response = requests.get(url=URL, headers=HEADERS)

soup = BeautifulSoup(response.content, "lxml")
# print(soup.prettify())

title = soup.find(id="productTitle").get_text().strip()
print(title)
price = soup.find(name="span", class_="a-offscreen").get_text()
print(price)
price = float(price.strip("$"))

if price <= TARGET_PRICE:
    message = f"Item is now {price}"

    with smtplib.SMTP(EMAIL_ENDPOINT, port=587) as connection:
        connection.starttls()
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg=f"Subject: Amazon price alert!\n\n{message}\n{url}")
