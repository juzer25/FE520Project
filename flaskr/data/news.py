## will use BeautifulSoup to get all the data from Yahoo finance
from bs4 import BeautifulSoup
import requests

def getNews():
    ##using BeautifulSoup
    res = requests.get('https://news.yahoo.com/')
    soup = BeautifulSoup(res.text, "html.parser")
    #val = soup.find()
    '''data = soup.find('div' , {"id": "mrt-node-YDC-Stream"})
    #print(data.find_all("div" , class_ = "Cf"))
    data = data.find('div', {"id": "YDC-Stream-Proxy"})

    data = data.find('div', {"id":"YDC-Stream"})
    data = data.find("ul", {"class":"My(0) P(0) Wow(bw) Ov(h)"})
    data = data.find_all("li")
    for i in data:
        print("-------------------")
        print(i)
        print("---------------------")'''
    #news = data.find('ul', {"class" : "My(0) P(0) Wow(bw) Ov(h)"})
    '''newsDict = {}
    i = 0
    for new in news:
        newsDict[i] = soup.prettify(new)
        i += 1
    #print(news,"\n")'''

    news_articles = soup.find_all("h3", class_="Mb(5px)")
    res = []
    newsDict = {}
    i = 0
    for news in news_articles:
       ''' res['title'] = news.a.text
        res['link'] = news.a['href']
        res['description'] = news.find_next('p').text.strip()
        res['image'] = news.find_previous("img")['src']
        newsDict[i] = res
        i += 1'''
       res.append({"title":news.a.text, "link":news.a['href'], 
                   "description":news.find_next('p').text.strip(),
                   "image":news.find_previous("img")['src']})

    return res

'''if __name__ == '__main__':
    print(getNews())'''