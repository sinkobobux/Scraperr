import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

urls=[f"https://kathmandupost.com/",f"https://thehimalayantimes.com/",f"https://english.onlinekhabar.com/"]
per_site=[]
suburls=[]
text=[]
avoid=["tag/","opinion/"]
trigger_words=["election","elections","party"]
output_dir="extracted_stuff"
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

def get_url():
    for url in urls:
        per_site.clear()
        response=requests.get(url)
        content = BeautifulSoup(response.text,"html.parser")
        for link in content.find_all('a'):
            if any(t_word in link.text.lower() for t_word in trigger_words):
                #print (link.text)
                absolute_url = urljoin(url,link.get('href'))
                if absolute_url not in per_site and all(avoid_path not in urlparse(absolute_url).path for avoid_path in avoid):
                    print(absolute_url)
                    per_site.append(absolute_url)
                if len(per_site)>2:
                    break
        suburls.append(per_site.copy())


def get_body():
    #print(suburls)
    for site in suburls:
        for i,url in enumerate(site):
            text.clear()
            response=requests.get(url)
            content=BeautifulSoup(response.text,"html.parser").find_all('p')
            for paragraph in content:
                text.append(paragraph)
            with open(f"{output_dir}/{urlparse(url).netloc}-{i}.txt",'w') as f:
                for paragraph in text:
                    f.write(paragraph.get_text(strip=True))

def main():
    get_url()
    get_body()


if __name__=="__main__":
    main()