import sqlite3
import os
from PIL import Image

# connect to database
database = sqlite3.connect("img_info.sqlite3")
# create cursor
cursor = database.cursor()


# initialize database
def init():
    # create table if not exists
    try:
        cursor.execute("""CREATE TABLE img (NAME text, TYPE text, FORMAT text, PATH text, img_x int, img_y int)""")
        database.commit()
        print("Table created")
    except sqlite3.OperationalError:
        print("Table already exists")
    # change working directory
    os.chdir("img")


def scan_path():
    # get all files in path
    os_files = set(os.listdir())
    # get all files in database
    db_files = set([i[0][4:] for i in cursor.execute("SELECT PATH FROM img").fetchall()])
    # get files to add
    add_files = os_files.difference(db_files)
    # get files to remove
    remove_files = db_files.difference(os_files)
    if len(add_files) == 0 and len(remove_files) == 0:
        print("No changes detected")
    else:
        # add files
        for file in add_files:
            # get image size
            img = Image.open(file)
            img_x, img_y = img.size
            # get image name
            name = file.split(".")[0]
            # get image type
            type = input("Enter type for %s (supported type: acg, wallpaper, avatar): " % name)
            # get image format
            format = file.split(".")[1]
            # get image path
            path = "img/" + file
            # insert into database
            cursor.execute("""INSERT INTO img VALUES (?, ?, ?, ?, ?, ?)""", (name, type, format, path, img_x, img_y))
            database.commit()
            print("Added %s" % file)
        # remove files
        for file in remove_files:
            # get image path
            path = "img/" + file
            # remove from database
            cursor.execute("DELETE FROM img WHERE PATH = ?", (path,))
            database.commit()
            print("Removed %s" % file)


def search():
    # get search term
    cursor.execute("""SELECT * FROM img""")
    # show results
    print(cursor.fetchall())


def manage():
    while True:
        # get user input
        print("\n1. Rescan Path")
        print("2. Search")
        print("3. Exit")
        choice = int(input("Enter choice: "))
        # insert image
        if choice == 1:
            scan_path()
            # search
        elif choice == 2:
            search()
        # exit
        elif choice == 3:
            break
        # invalid input
        else:
            print("Invalid choice")


if __name__ == "__main__":
    # initialize database
    init()
    # manage database
    manage()
    # close database and exit
    cursor.close()
    database.close()
