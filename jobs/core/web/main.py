import requests
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup

from jobs.core.log.logger import setup_logger

log = setup_logger('core')

class webScrapping:

    def __init__(self):
        pass

    def get(self,url):
        log.info(url)
        site = urlopen(url)
        site = BeautifulSoup(site,'lxml')
        return site

    def getImage(self,url,file):
        log.info(url)
        log.info(file)
        r2 = requests.get(url)
        with open(file, "wb") as f:
            f.write(r2.content)
        return file

    def getImageV2(self,url,file):
        log.info(url)
        log.info(file)
        urllib.request.urlretrieve(url,file)
