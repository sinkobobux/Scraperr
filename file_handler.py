import json
import os
from urllib.parse import urlparse

output_dir="extracted_stuff"
json_path=os.path.join(output_dir,"output.json")

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

def store_json(scraped_stuff):
    try:
        with open(json_path,'w',encoding='utf-8') as f:
            json.dump(scraped_stuff,f,ensure_ascii=False,indent=4)
    except Exception as e:
        print(f"Couldn't dump to json: {e} occured")
    else:
        print(f"Dumped to {json_path}")
    
def store_text(scraped_stuff):
    for i, page_data in enumerate(scraped_stuff):
        url=page_data['Url']
        headline=page_data["Headline"]
        body=page_data['Body']
        file_path=f"{output_dir}/{i} - from {urlparse(url).netloc}.txt"
        try:
            with open(file_path,'w') as f:
                f.write(headline.strip()+"\n\n"+body)
        except Exception as e:
            print(f"Couldnt't write to file: {e} occured")
        else:
            print(f"Written to {file_path}")
        