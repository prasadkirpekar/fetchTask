from os import path, remove
from os import path, remove
import requests
from urllib.parse import urlparse
from datetime import datetime
import sys


#common logics can be added here
class Helper():
    def __init__(self) -> None:
        pass

    def getFileNameFromUrl(self,url):
        return self.getDomainFromUrl(url)+".html"
    
    def getDomainFromUrl(self,url):
        return urlparse(url).netloc


class MetaData:
    __url = ""
    __images = 0
    __links = 0
    __lastFetch = ""

    def __init__(self,url) -> None:
        self.__url = url
        self.genMetaData()

    def genMetaData(self):
        filePath = "./"+Helper().getFileNameFromUrl(self.__url)
        self.__lastFetch=datetime.fromtimestamp(path.getmtime(filePath))
        self.__lastFetch = self.__lastFetch.strftime("%a %b %d %Y %H:%M %Z")
        domainFile = open(filePath,"r")
        domainData = domainFile.read()
        self.__links = domainData.count("<a href")
        self.__images = domainData.count("<img src")
    
    def __str__(self) -> str:
        strOutput = "site: "+Helper().getDomainFromUrl(self.__url)+"\n"
        strOutput += "num_links: "+str(self.__links)+"\n"
        strOutput += "images: "+str(self.__images)+"\n"
        strOutput += "last_fetch: "+str(self.__lastFetch)+"\n"
        return strOutput


class Fetch:
    __url=""
    def __init__(self,url) -> None:
        self.__url = url
    
    def performFetch(self):
        domainFile = "./"+Helper().getFileNameFromUrl(self.__url)
        try:
            req = requests.get(self.__url, 'html.parser')
            if path.exists(domainFile):
                remove(domainFile)
            with open(domainFile, 'w') as f:
                f.write(req.text)
                f.close()
        except Exception as error:
            print(str(error))

class Driver:
    
    __parameters = []
    __stack = []
    
    def __init__(self,parameters):
        self.__parameters = parameters
    

    def isOption(self,param):
        return param.find("--")==0

    def processOption(self,option,url):
        option = option.lower()
        if option == '--metadata':
            metaData = MetaData(url)
            print(str(metaData))
        # more options can be added here

    def performOperation(self):
        parameters = self.__parameters
        for i in range(1,len(parameters)):
            param = parameters[i]
            if self.isOption(param):
                self.__stack.append(param)
            elif self.__stack and self.isOption(self.__stack[-1]):
                self.processOption(self.__stack[-1],param)
                self.__stack.pop()  # last used option can be popped from here
            else:
                Fetch(param).performFetch() # fetch url from the internet



parameters = sys.argv
driver = Driver(parameters)
driver.performOperation()

#examples
#   python3 fetch.py https://google.com https://facebook.com
#   python3 fetch.py --metadata https://google.com --metadata  https://facebook.com