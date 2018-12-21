from bs4 import BeautifulSoup as soup
from requests import get
import pandas as pd
import time
from IPython.core.display import clear_output
from random import randint
import datetime


keyword = input("What is the keyword you wanna look up?(e.g 'paro' o 'huelga de maestros')\n")

titles = []
links = []
contents = []
dates = []
start_time = time.time()
requests = 0
pages = [str(i) for i in range(33,5500)]
count = 0
repeat = ''
done = False

for page in pages:
    
    page = str(int(page)-1)
    url = "https://www.vanguardia.com/search/node/" + keyword + "?page=" + page
    print(url)
    html = get(url)
    htmlsoup = soup(html.content,'html.parser')
    time.sleep(randint(2,4))
    requests += 1
    count += 1
    contador=1
    elapsed_time = time.time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)
    articles = htmlsoup.find_all('div', class_="resultado")
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
            title = oneArticle.a.text
            if contador == 1 :
                if title == repeat :
                    done = True
                    break
                else :
                    repeat=title
            link = oneArticle.a['href']
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
            especial=noodles.find_all('p')
            if len(especial) != 0 :
                date = htmlsoup.find('div',class_="fecharesult").text
                date = date[:-5]
                date = date.replace(" de "," ")
                titles.append(title)
                texto=''
                for textos in especial:
                    texto=texto+textos.getText()
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
            contador += 1
            
    if done:
        print("There were no more articles found with your keyword")
        break
    if count==10 :
        test_df.to_excel("vanguardia_" + keyword + ".xlsx")   
        count=0
      
test_df.to_excel("vanguardia_" + keyword + ".xlsx")     
