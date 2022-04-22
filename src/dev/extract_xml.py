from bs4 import BeautifulSoup
import codecs
import lxml

afg_url = r'C:\Users\adanzun\OneDrive\Home Lab\AFG\12.5\clusterConfig.html'


soup = BeautifulSoup(codecs.open(afg_url, 'r'), features='html.parser')

html_body = soup.find('body')

x = html_body.findChildren(recursive=False)[0]

print(x.text)
# xml_soup = BeautifulSoup(x.contents()[0], features='lxml')
#
# print(xml_soup.prettify())
