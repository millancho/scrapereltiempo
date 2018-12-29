#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

titles = []
dates = []
links = []
contents = []
keyword = input("What is the keyword you wanna look up?(e.g 'paro' o 'huelga de maestros')\n")
pages = [str(i) for i in range(1,5000)]
browser = webdriver.Chrome()
count = 0

for page in pages:
    
    count += 1
    browser.get("https://elpais.com/buscador/?qt=" + keyword + "&sf=0&np=" + page + "&bu=ep&of=html")
    time.sleep(2)
    browser.refresh()
    html = browser.page_source
    soup = bs(html, 'html5lib')
    containers = soup.find_all('div', class_="article")
    if len(containers) != 0:
        for container in containers:
            titulo = container.find('h2').a.text
            fecha = container.find('span', attrs={'class':'fecha'}).text
            link = "http://elpais.com" + container.find('h2').a['href']
            browser.get(link)
            time.sleep(2)
            browser.refresh()
            html2 = browser.page_source
            soup2 = bs(html2, 'html5lib')
            content = soup2.find('div', attrs={'class':'articulo-cuerpo'})
            if content != None :
                textos = content.find_all('p')
                if len(textos) != 0:
                    texto = ''
                    for text in textos:
                        texto += text.getText()
                else:
                    texto = "Especial"
            else:
                texto = "Especial"
            contents.append(texto)
            titles.append(titulo)
            dates.append(fecha)
            links.append(link)
        resultados = pd.DataFrame({'Titulo':titles,
                                'Fecha':dates,
                                'Link':links,
                                'Contenido':contents})
    else:
        print("There were no more articles found for your keyword")
        break
    if count == 5:
        count = 0
        resultados.to_excel("elpais_" + keyword + ".xlsx")
resultados.to_excel("elpais_" + keyword + ".xlsx")

