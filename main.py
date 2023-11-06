import json
import os 
import requests 
import pandas as pd
from auth_data import token
from urllib.parse import urlparse, parse_qs



def get_wall_posts(group_name):
    url = f"https://api.vk.com/method/video.get?owner_id=-64212668&album_id={group_name}&count=100&access_token={token}&v=5.131"
    req = requests.get(url)
    src = req.json()
    
    # проверка есть ли проект 
    if os.path.exists(f"{group_name}"):
        print(f"Папка с именем {group_name} существует")
    else:
        os.mkdir(group_name)
        
    # Сохраняем в json 
    with open(f"{group_name}/{group_name}.json", "w", encoding="utf-8") as file:
              json.dump(src, file, indent=4, ensure_ascii=False)
    
    
    # ID video
    
    posts = src["response"]["items"]
    
    fresh_posts_id = [post["title"] for post in posts]
    video_links_id = [video["player"] for video in posts]
    # Сокращаем link
    short_video_link = []
    for link in video_links_id:
        parsed_url = urlparse(link)
        parsed_qs = parse_qs(parsed_url.query)
        shorted_link = f"oid={parsed_qs['oid'][0]}&id={parsed_qs['id'][0]}&hash={parsed_qs['hash'][0]}"
        short_video_link.append(shorted_link)
        
    
    
    data = {"Название": fresh_posts_id, "Ссылка": short_video_link}
    df = pd.DataFrame(data)
    df.to_csv(f"{group_name}/exist_posts_{group_name}.csv", index=False)
    

def main():
    group_name = input("Введите ID альбома: ")
    get_wall_posts(group_name)
    
if __name__ == "__main__":
    main()