import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

urls=[f"https://kathmandupost.com/","https://thehimalayantimes.com/","https://english.onlinekhabar.com/"]
per_site=[]
suburls=[]

trigger_words=["election","elections","party","rsp","uml","congress"]

for url in urls:
    response=requests.get(url)
    content = BeautifulSoup(response.text,"html.parser")
    for link in content.find_all('a'):
        if any(t_word in link.text.lower() for t_word in trigger_words):
            #print (link.text)
            per_site.append(urljoin(url,link.get('href')))
            if len(per_site)>3:
                break
    suburls.append(per_site)


print(suburls)