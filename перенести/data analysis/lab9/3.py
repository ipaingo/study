import bs4
from bs4 import BeautifulSoup

import requests
import lxml
import html5lib
import re 

html_doc = ""

with open("lab_works_files/Карелия_википедия.html", "r", encoding='utf-8') as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, 'html.parser')
lnks = list(filter(lambda x: 'href' in x.attrs and x['href'].startswith("/wiki/"), soup.find_all("a")))
# lnks = [x.attrs['href'] for x in soup.find_all("a") if ]
dct = {x.text: x for x in lnks}

print(dct["Музыкальный театр Республики Карелия"])

print("/wiki/%D0%9C%D1%83%D0%B7%D1%8B%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D1%82%D0%B5%D0%B0%D1%82%D1%80_%D0%A0%D0%B5%D1%81%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B8_%D0%9A%D0%B0%D1%80%D0%B5%D0%BB%D0%B8%D1%8F")