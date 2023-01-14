import requests
import bs4
from bs4 import BeautifulSoup

# a program, that searches for a specific element
# the final aim was to create a better "kanttiinit.fi"
# type of website. However, I deemed this project not
# worth the effort

def findWord(word, text):
    length = len(word)
    tot = 0
    counter = 0
    while (counter-tot+length <= len(text)):
        if text[counter].lower() == word[tot].lower():
            tot += 1
            if tot == length:
                break
        else:
            if tot != 0:
                counter -= 1
            tot = 0
        counter += 1
    return counter-length+1, tot == length #jos jälkimmäinen True sana alkaa palautuksen indeksiltä


kvarkki = "https://www.sodexo.fi/ravintolat/ravintola-aalto-kvarkki"
tuas = "https://www.foodandco.fi/ravintolat/Ravintolat-kaupungeittain/espoo/aalto-yliopisto-tuas/"

page = requests.get(tuas)
soup = BeautifulSoup(page.content, 'html.parser')
divs = list(soup.find_all('div'))
spans = list(soup.find_all('span'))
smalls = list(soup.find_all('class'))
children = list(soup.children)
searchWord = "kasvispata"
print(len(children))

positions = []
for i in range(len(spans)):
    temp = findWord(searchWord, spans[i].get_text())
    print(spans[i])
    if temp[1]:
        positions.append([i, temp[0]])

'''tag = page.soup.select("#result")[0]
result = tag.text'''

print(len(positions))
#class="meal-name ng-binding"
#soup.find_all("div", class_="stylelistrowone stylelistrowtwo")
myspans2 = soup.find_all("span.meal-name.ng-binding") #TODO: täs linkis on search by CSS-class, se vois tomii. https://www.crummy.com/software/BeautifulSoup/bs4/doc/#method-names
myspans = soup.find_all('span', class_='meal-name ng-binding')
mydivs = soup.find_all("div", class_="menu-container-set-menu-content")
print(len(myspans2), len(mydivs), len(myspans))
'''for i in range(len(mydivs)):
    print(mydivs[i].get_text())
    print("--------------")'''
tag = soup.select("#meal-name ng-binding")
print(len(tag))

css_soup = BeautifulSoup('"span", class_="meal-name ng-binding"></p>', 'html.parser')
print(len(css_soup))
print(css_soup.get_text())
#css_soup = BeautifulSoup('<p class="body strikeout"></p>', 'html.parser')
