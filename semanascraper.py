from bs4 import BeautifulSoup as soup
import pandas as pd
import time
from IPython.core.display import clear_output
from random import randint
import datetime
from selenium import webdriver

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%m/%d/%Y')
        return True
    except ValueError:
        return False

now=datetime.datetime.now()
dia=str(now)
dia=dia[2:10]

keyword = input("What is the keyword you wanna look up?(e.g 'paro' o 'huelga de maestros')\n")

titles = []
links = []
contents = []
dates = []

start_time = time.time()
requests = 0
pages = [str(i) for i in range(1,5500)]
count = 0

options=webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome(options=options)

for page in pages:
    page=str((int(page)-1)*10)
    url = "https://www.semana.com/Buscador?query=" + keyword + "&post=semana&limit=10&offset=" + page + "&from=2000%2F01%2F01&facet0=type%2FArt%C3%ADculo"
    print(url)
    browser.get(url)
    time.sleep(2)
    browser.refresh()
    html = browser.page_source
    htmlsoup = soup(html, 'html5lib')
    time.sleep(randint(2,4))
    requests += 1
    count += 1
    elapsed_time = time.time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)
    articles=htmlsoup.find_all('div',class_="result")
    if (len(articles) == 0):
        print(requests)
        print("There were no more articles found with your keyword")
        test_df=pd.DataFrame({'Titulo':titles,
                                  'Fecha':dates,
                                  'Contenido':contents,
                                  'Link':links})
        break
    else:   
        for oneArticle in articles:
            link = oneArticle.a['href']
            content = ''
            url2 = link
            link = ''
            while link == '':
                try:
                    browser.get(url2)
                    link = browser.page_source
                    break
                except:
                    print("Connection refused by the server")
                    time.sleep(3)
                    print("Let's try again...")
                    continue
            print(url2)    
            noodles=soup(link,'html5lib')
            noodles.find_all
            content=noodles.find_all('div', id="contentItem")
            if len(content) != 0 :
                tipo=''
                date = noodles.find('span', class_="date").text.strip()
                date=date[2:15]
                date=date.replace(" ", "  ")
                date=date[0:10].replace(" ","")
                if validate(date)==True:
                    objDate = datetime.datetime.strptime(date, '%m/%d/%Y')
                    strDate = datetime.datetime.strftime(objDate, '%b %d %Y')
                else:
                    objDate = datetime.datetime.strptime(date, '%Y/%m/%d')
                    strDate = datetime.datetime.strftime(objDate, '%b %d %Y')
                    
                title = ''
                
                if noodles.find('h1', class_="tittleArticuloOpinion") != None:
                    title = noodles.find('h1', class_="tittleArticuloOpinion").text.strip()
                else:
                    if noodles.find('h1', class_="nameColumnista") != None:
                        title = noodles.find('h1', class_="nameColumnista").text.strip()
                    if noodles.find('h2', class_ = "article-h") != None:
                        title = noodles.find('h2', class_ = "article-h").text.strip()
                                     
                    
                titles.append(title)
                texto=''
                for textos in content:
                    texto=texto+textos.getText()
                texto=texto.replace('\n','').strip()
                contents.append(texto)
                dates.append(strDate)
                links.append(url2)
                  
                
                test_df=pd.DataFrame({'Titulo':titles,
                              'Fecha':dates,
                              'Contenido':contents,
                              'Link':links})
    
            else :
                date = 0
                titles.append(title)
                content="Especial"
                contents.append(content)
                dates.append(date)
                links.append(url2)
                
                test_df=pd.DataFrame({'Titulo':titles,
                              'Fecha':dates,
                              'Contenido':contents,
                              'Link':links})
            
    if count==10 :
        test_df.to_excel("semana_" + keyword + ".xlsx")   
        count=0
      
test_df.to_excel("semana_" + keyword + ".xlsx")     
