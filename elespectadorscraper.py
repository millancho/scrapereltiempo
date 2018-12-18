from bs4 import BeautifulSoup as soup
from requests import get
import pandas as pd
import time
from IPython.core.display import clear_output
from random import randint


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
    
    url = "https://www.elespectador.com/search/" + keyword + "?page=" + page
    html = get(url)
    htmlsoup = soup(html.content,'html.parser')
    time.sleep(randint(2,4))
    requests += 1
    count += 1
    elapsed_time = time.time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)
    articles = htmlsoup.find_all('div', class_="node-title field field--name-title field--type-ds field--label-hidden")
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
            title = oneArticle.a.text.strip()
            link = oneArticle.a['href']
            content = ''
            url2 = "http://www.elespectador.com" + link
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
            especial=noodles.find('div',class_="node-body content_nota field field--name-body field--type-text-with-summary field--label-hidden")
            if especial != None :
                content=especial.find_all('p')
                if content != None:
                    date = noodles.find('div',class_="node-post-date field field--name-post-date field--type-ds field--label-hidden").text
                    date = date[:-11]
                    titles.append(title)
                    texto=''
                    for textos in content:
                        texto=texto+textos.getText()
                    texto=texto.replace('\n','')
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
        test_df.to_excel("elespectador_" + keyword + ".xlsx")   
        count=0
      
test_df.to_excel("elespectador_" + keyword + ".xlsx")     
