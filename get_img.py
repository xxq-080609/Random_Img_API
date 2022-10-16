import os
import requests
import sqlite3
import json
from PIL import Image

database = sqlite3.connect("img_info.sqlite3")
cursor = database.cursor()


def get_acg():
    while True:
        try:
            context = requests.get("https://api.lolicon.app/setu/v2?size=original&size=regular&r18=0").text
            pid = json.loads(context)['data'][0]['pid']
            name = json.loads(context)['data'][0]['title']
            rt = os.system(f"wget https://pixiv.cat/{pid}.jpg")
            if rt == 0:
                img = Image.open(f'./{pid}.jpg')
                img_x, img_y = img.size
                cursor.execute("""INSERT INTO img VALUES (?, ?, ?, ?, ?, ?)""",
                               (name, 'acg', 'jpg', f'img/{pid}.jpg', img_x, img_y))
                database.commit()
        except KeyboardInterrupt:
            break


def get_img():
    os.chdir("img")
    while True:
        print("\nPrint in the type of image you want to get.")
        print("1. acg")
        print("2. wallpaper")
        print("3. avatar")
        print("4. exit")
        choice = int(input("Enter choice: "))
        match choice:
            case 1:
                get_acg()
            case 2:
                pass
            case 3:
                pass
            case 4:
                break
            case _:
                print("Invalid choice")


if __name__ == "__main__":
    get_img()
