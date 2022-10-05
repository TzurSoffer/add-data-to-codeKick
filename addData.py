import json

from scrapeGithubUsingSelenium import *
from sortFiles import *
import loading

basePath = "data/"
email = input("GitHub email: ")
password = input("GitHub password: ")
topic = input("topic: ")
linksFile = topic+"Links.json"
category = input("category: ")
dataFile = "data"+topic[0].upper()+topic[1:]

loader = loading.LoadingSpin()
loader.start()

getLinks = ScrapeGithubForLinks(githubEmail=email, githubPassword=password, type=Type.code, linksFile = "./data/"+linksFile)
getLinks.getLinks(topic=topic, endPage= 100, startPage=1)
getLinks.quit()
linkScraper = ScrapeGithubLinks(linksFile = linksFile, dataFile = basePath+dataFile+".json")
linkScraper.scrapeLinks()


with open(basePath+dataFile+".json", "r") as f:
    jsonFile = json.load(f)

data = []
for i in jsonFile:
    text = jsonFile[i]
    objectFinder = FindObjectInText(text, category)
    data.append(objectFinder.findTerms())

    
with open(basePath+dataFile+"Organized.json", "w") as f:
    json.dump(data, f)

loader.stop()
print("done")
#print(len(str(data)))
