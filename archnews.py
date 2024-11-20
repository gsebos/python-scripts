from bs4 import BeautifulSoup
import requests

URL = "https://archlinux.org/"

try:
    response = requests.get(URL)
except:
    print(f"error with the URL, no response")
    exit()
if response.status_code == 200:
    html = response.content
    soup = BeautifulSoup(html,features="html.parser")
    
    news = soup.find('div',class_='article-content').find('p').text
    date = soup.find('h4').find('a').find_next('p').text
    
    print(f"Latest Arch Wiki News: {date} - {news}")
else:
    print(f"Error, response status code {response.status_code}")