import time
import json

import requests
from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def removeDuplicates(listToRemoveDuplicates) -> list:
    newList = []
    for lists in listToRemoveDuplicates:
        for l in lists:
            if l not in newList:
                newList.append(l)
    return(newList)

class Type():
    repository = "Repository"
    code = "Code"

class ScrapeGithubForLinks():
    def __init__(self, githubEmail, githubPassword, startingPage = 1, linksFile = "links.json", language = "Python", type = Type.repository):
        self.githubEmail = githubEmail
        self.githubPassword = githubPassword
        self.currentPage = startingPage
        self.language = language
        self.linksFile = linksFile
        self.type = type

        self.driver = webdriver.Chrome(".\chromedriver.exe")
        self.login()

    def nextPage(self):
        self.gotoPage(self.currentPage+1)
    
    def previusPage(self):
        self.gotoPage(self.currentPage-1)
    
    def gotoPage(self, page):
        self.currentPage = page

    def login(self):
        self.driver.get("https://github.com/login")
        self.driver.find_element(By.NAME, "login").send_keys(self.githubEmail)
        self.driver.find_element(By.NAME, "password").send_keys(self.githubPassword)
        self.driver.find_element(By.NAME, "commit").click()

    def getCurrentPageLinks(self, topic) -> list:
        url = "https://github.com/search?l=%s&p=%d&q=%s&type=%s" %(self.language, self.currentPage, topic, self.type)
        links = []
        self.driver.get(url)
        source = self.driver.page_source
        soup = bs(source, "lxml")
        #page = self.driver.find_element_by_tag_name("body")
        linksFrame = soup.find_all("div", "f4 text-normal")
        for link in linksFrame:
            links.append("https://github.com/"+link.find("a")["href"])


        return(links)

    def getLinks(self, topic, endPage, startPage = 1, save = True) -> list: # returns the href links in selected pages
        try:
            links = []
            self.currentPage = startPage
            for _ in range(startPage, endPage):
                link = self.getCurrentPageLinks(topic)
                if link == []:
                    time.sleep(20)
                    self.previusPage()
                
                links.append(link)
                self.nextPage()
            
            links = removeDuplicates(links)
        
        except Exception as e:
            print(e)

        finally:
            if save:
                with open(self.linksFile,"w") as f:
                    json.dump(links, f)
            
            return(links)

    def quit(self):
        self.driver.quit()

class ScrapeGithubLinks():
    def __init__(self, linksFile = "links.json", dataFile = "data.json"):
        self.linksFile = linksFile
        self.dataFile = dataFile

    def scrapeLinks(self, fromLinks = True, save = True):
        currentJsonIndex = 0
        jsonData = {}

        if fromLinks:
            with open(self.linksFile, "r") as f:
                links = json.load(f)
        
        else:
            links = fromLinks

        for link in links:
            link = link.replace("https://github.com/", "https://raw.githubusercontent.com/", 1).replace("blob/", "", 1)
            print(link)
            r = requests.get(link)
            if r.status_code != 200:
                print("error:\n")
                continue

            text = bs(r.content, "lxml").text
            jsonData[currentJsonIndex] = text
            currentJsonIndex += 1
        
        if save:
            with open(self.dataFile, "w") as f:
                json.dump(jsonData, f)

        return(jsonData)