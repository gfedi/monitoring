from bs4 import BeautifulSoup
import sys
import urllib2
import requests

#url = 'http://192.168.0.10/protect/CMUConfig.htm?AllOn=All+PSU+ON'
url = 'http://192.168.0.20/INDEX.HTM'
username = 'admin'
password = 'admin'
html_doc = requests.get(url, auth=(username, password)).content

print(html_doc)








