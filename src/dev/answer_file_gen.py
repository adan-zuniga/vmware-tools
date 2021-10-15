from requests import get
from bs4 import BeautifulSoup

afg_url = 'https://www.cisco.com/c/en/us/applicat/content/cuc-afg/index.html'

res = get(url=afg_url)
soup = BeautifulSoup(res.content, features='html.parser')
print(soup.prettify())
