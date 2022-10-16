from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from typing import Union
from re import match
import sqlite3
from random import choice
from enum import Enum
import os

# init app
app = FastAPI()
# connect to database
database = sqlite3.connect("img_info.sqlite3")
# create cursor
cursor = database.cursor()
if not os.path.exists("img"):
    os.mkdir("img")


class AvailableTypes(str, Enum):
    acg = "acg"
    wallpaper = "wallpaper"
    avatar = "avatar"


# app routes
@app.get("/")
async def main(type_filter: Union[str, None] = Query(default=None, max_length=10, regex=r"^(acg|wallpaper|avatar)$"),
               size: Union[str, None] = Query(default=None, max_length=10, regex=r"^([1-9]\d*|\?)x([1-9]\d*|\?)$")):
    """
    available parameters:
    type_filter: filter by type, default is none, accepts string, available options are "acg", "wallpaper", "avatar"
    size: filter by size, default is none, accepts context string, format is [Number | ?]x[Number | ?], e.g. 1920x1080
    """
    # SELECT PATH, FORMAT FROM img [WHERE] [type = ""] [AND_1] [img_x = ""] [AND_2] [img_y = ""]
    search_args = []
    if type_filter is not None:
        search_args.append(f"TYPE = \"{type_filter}\"")
    if size is not None:
        match_size = match(r"([1-9]\d*|\?)x([1-9]\d*|\?)", size)
        if match_size.group(1) != "?":
            search_args.append(f"img_x = \"{match_size.group(1)}\"")
        if match_size.group(2) != "?":
            search_args.append(f"img_y = \"{match_size.group(2)}\"")
    if len(search_args) == 0:
        res = cursor.execute("SELECT PATH, FORMAT FROM img")
    elif len(search_args) == 1:
        res = cursor.execute("SELECT PATH, FORMAT FROM img WHERE %s" % search_args[0])
    else:
        print("SELECT PATH, FORMAT FROM img WHERE %s" % " AND ".join(search_args))
        res = cursor.execute("SELECT PATH, FORMAT FROM img WHERE %s" % " AND ".join(search_args))
    try:
        img = choice(res.fetchall())
    except IndexError:
        return {"error": "no image found"}
    file = open(img[0], "rb")
    # return image
    return StreamingResponse(file, media_type="image/" + img[1].lower())
