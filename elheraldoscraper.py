from bs4 import BeautifulSoup as soup
from requests import get
import pandas as pd
import time
from IPython.core.display import clear_output
from random import randint
import datetime
from collections import OrderedDict


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
    
    page = str(int(page)-1)
    url = "https://www.elheraldo.co/search?keyword=" + keyword + "&type=articulo&page=" + page
    print(url)
    html = get(url)
    htmlsoup = soup(html.content,'html.parser')
    time.sleep(randint(2,4))
    requests += 1
    count += 1
    elapsed_time = time.time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)
    articles = htmlsoup.find_all('div', class_="search-item")
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
            title = oneArticle.h2.a.text
            link = oneArticle.h2.a['href']
            content = ''
            url2 = link
            link = ''
            while link == '':
                try:
                    link = get(url2)
                    break
                except:
                    print("Connection refused by the server")
                    time.sleep(3)
                    print("Let's try again...")
                    continue
            print(url2)    
            noodles=soup(link.content,'html.parser')
            description=noodles.find_all('div',id="description")
            if len(description) != 0 :
                date = noodles.find('div',class_="date").text.replace('\n','')
                date=date[:-7].replace('|','').strip().replace(' de ',' ')
                titles.append(title)
                texto = ''
                for textos in description:
                    texto=texto+textos.getText()
                lista = []
                insidetexto = noodles.find_all('div', class_="field")
                for insidetextos in insidetexto:
                    lista.append(insidetextos.p)
                lista = filter(None,lista)              
                lista = list(OrderedDict.fromkeys(lista))
                for items in lista:
                    texto=texto+items.getText()
                texto = texto.replace('\n','')
                texto = texto.replace('\xa0','')
                contents.append(texto)
                dates.append(date)
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
        test_df.to_excel("elheraldo_" + keyword + ".xlsx")   
        count=0
      
test_df.to_excel("elheraldo_" + keyword + ".xlsx")     
