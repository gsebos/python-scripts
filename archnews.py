from bs4 import BeautifulSoup
import requests

URL = "https://archlinux.org/"

response = requests.get(URL)
html = response.content
soup = BeautifulSoup(html,features="html.parser")

news = soup.find('div',class_='article-content').find('p').text
date = soup.find('h4').find('a').find_next('p').text

print(f"Latest Arch Wiki News: {date} - {news}")