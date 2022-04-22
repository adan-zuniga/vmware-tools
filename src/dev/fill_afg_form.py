from requests import get, post, Session
from bs4 import BeautifulSoup

afg_url = 'https://www.cisco.com/c/en/us/applicat/content/cuc-afg/index.html'

res = get(url=afg_url)

soup = BeautifulSoup(res.content, features='html.parser')
forms = soup.findAll('form')

for field in forms[0]:
    if field.name:
        print(field)
        print('*' * 180)
    # if field.has_key('name'):
    #         print(field['name'])

print(soup.prettify())
html_body = soup.find('body')

# print(html_body.findChildren(recursive=False)[0])
# print(f.read())

data = {'hostNamePrimary': 'c1-cucm1'}

post_result = post(
    url=afg_url,
    data=data
)

print(post_result)

session = Session()
r = session.get(url=afg_url)

print(r)
