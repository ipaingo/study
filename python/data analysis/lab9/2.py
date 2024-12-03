import bs4
from bs4 import BeautifulSoup

import requests
import lxml
import html5lib
import re 

html_doc = ""

with open("lab_works_files/ПетрГУ_Википедия.html", "r", encoding='utf-8') as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, 'html.parser')

print(len(soup.find_all("a")))
print(len(soup.find_all("div")))

print(193 + 1926)