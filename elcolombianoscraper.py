from bs4 import BeautifulSoup as soup
from requests import get
import pandas as pd
import time
from IPython.core.display import clear_output
from random import randint
import datetime


now=datetime.datetime.now()
dia=str(now)
dia=dia[0:10].replace('-','')

keyword = input("What is the keyword you wanna look up?(e.g 'paro' o 'huelga de maestros')\n")

titles = []
links = []
contents = []
dates = []

start_time = time.time()
requests = 0
pages = [str(i) for i in range(1,5500)]
count = 0

for page in pages:
    
    url = "http://www.elcolombiano.com/busqueda/-/search/" + keyword + "/false/true/20000101/" + dia + "/date/true/true/0/0/meta/0/0/5/" + page
    html = get(url)
    htmlsoup = soup(html.content,'html.parser')
    time.sleep(randint(2,4))
    requests += 1
    count += 1
    elapsed_time = time.time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)  
    print(url)
    articles = htmlsoup.find_all('div', class_="noticia-resultado")
    if len(articles) != 0:
        for oneArticle in articles:
                
            title = oneArticle.h3.text.strip()
            link = oneArticle.a['href']
            if "ecbloguer" in link :
                date = oneArticle.span.text.strip()
                content=''
                titles.append(title)
                contents.append(content)
                dates.append(date)
                links.append(link) 
                test_df=pd.DataFrame({'Titulo':titles,
                              'Fecha':dates,
                              'Contenido':contents,
                              'Link':links})
                
            else :
                date = oneArticle.span.text.strip()
                content = ''
                url2 = "http://www.elcolombiano.com"  + link
                link = ''
                print(url2)
                while link == '':
                    try:
                        link = get(url2)
                        break
                    except:
                        print("Connection refused by the server")
                        time.sleep(3)
                        print("Let's try again...")
                        continue
                noodles=soup(link.content,'html.parser')
                especial=noodles.find_all('div', "text")
                
                if len(especial) != 0 :
                    for texto in especial:
                        content+=texto.getText()
                    titles.append(title)
                    contents.append(content)
                    dates.append(date)
                    links.append(url2) 
                    test_df=pd.DataFrame({'Titulo':titles,
                                  'Fecha':dates,
                                  'Contenido':contents,
                                  'Link':links})
            
                else :
                    titles.append(title)
                    dates.append(date)
                    content="Especial"
                    contents.append(content)
                    links.append(url2)
                    
                    test_df=pd.DataFrame({'Titulo':titles,
                                  'Fecha':dates,
                                  'Contenido':contents,
                                  'Link':links})
    else:
        test_df=pd.DataFrame({'Titulo':titles,
                                  'Fecha':dates,
                                  'Contenido':contents,
                                  'Link':links})
        print("There were no more articles found with your keyword")
        break
        
            
if count==10 :
    test_df.to_excel("elcolombiano_" + keyword + ".xlsx")   
    count=0
  
test_df.to_excel("elcolombiano_" + keyword + ".xlsx")     
