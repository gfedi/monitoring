from bs4 import BeautifulSoup
import sys
import urllib2
import requests

#url = 'http://192.168.0.10/protect/CMUConfig.htm?AllOn=All+PSU+ON'
url = 'http://192.168.0.10/protect/CMUConfig.htm?AllOff=All+PSU+OFF'
username = 'meanwell'
password = 'meanwell'
html_doc = requests.get(url, auth=(username, password)).content

print(html_doc)








