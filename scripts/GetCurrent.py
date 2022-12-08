from bs4 import BeautifulSoup
import sys
import urllib2
import requests

#url = 'http://192.168.0.10/protect/CMUConfig.htm?AllOff=All+PSU+OFF'
url = 'http://192.168.0.10/status.xml' 
username = 'meanwell'
password = 'meanwell'
html_doc = requests.get(url, auth=(username, password)).content

soup = BeautifulSoup(html_doc, 'xml')
field = soup.find_all('Current0')[0].get_text()

print(field)







