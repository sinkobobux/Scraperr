import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
from file_handler import store_json, store_text
import sys

urls=[f"https://kathmandupost.com/",f"https://thehimalayantimes.com/",f"https://english.onlinekhabar.com/"]
avoid=["tag/","opinion/"]
trigger_words=["election","elections","party"]

def get_url():
    per_site=[]
    links=[]
    for url in urls:
        per_site.clear()
        response=requests.get(url)
        content = BeautifulSoup(response.text,"html.parser")
        for link in content.find_all('a'):
            if any(t_word in link.text.lower() for t_word in trigger_words):
                absolute_url = urljoin(url,link.get('href'))
                if absolute_url not in per_site and all(avoid_path not in urlparse(absolute_url).path for avoid_path in avoid):
                    per_site.append((link.text,absolute_url))
                if len(per_site)>2:
                    break
        links.append(per_site.copy())
    return links

def get_body(links):
    scraped_stuff = []
    for site in links:
        for (headline,url) in site:
            response=requests.get(url)
            content=BeautifulSoup(response.text,"html.parser").find_all('p')
            body = ' '.join([paragraph.get_text(strip=True) for paragraph in content])
            page_data = {'Headline':headline.strip(), 'Body': body,'Url': url}
            scraped_stuff.append(page_data)
    return scraped_stuff        

def main(json=False):
    links=get_url()
    scraped_stuff = get_body(links)
    if json:
        store_json(scraped_stuff)
    else:
        store_text(scraped_stuff)

if __name__=="__main__":
    parser=argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--json",help="Store scraped data in a json file", action = 'store_true')
    parser.add_argument("--text",help="Store scraped data in a text files", action = 'store_true')
    try:
        args=parser.parse_args()
        if args.json and args.text:
            raise Exception(f"Can't use both arguments {sys.argv[1]} and {sys.argv[2]}")
        elif args.json:
            main(True)
        else:
            main()
    except Exception as e:
        print(e)
    except:
        print("Unsupported arguments")