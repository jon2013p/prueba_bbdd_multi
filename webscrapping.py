import requests
from bs4 import BeautifulSoup
# Import MongoClient from pymongo so we can connect to the database
from pymongo import MongoClient




if __name__ == '__main__':
    # Instantiate a client to our MongoDB instance
    db_client = MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false")
    bddmongo2 = db_client.bddmongo2
    posts = bddmongo2.posts


    response = requests.get("https://www.wattpad.com/stories/aventura")
    soup = BeautifulSoup(response.content, "lxml")

    post_titles = soup.find_all("a", class_="title meta on-story-preview")

    extracted = []
    for post_title in post_titles:
        extracted.append({
            'title' : post_title.text,
            'link'  : post_title["/story/130579579-bad-boy-peligro-1-completa"]
        })

    # Iterate over each post. If the link does not exist in the database, it's new! Add it.
    for post in extracted:
        if db_client.bddmongo2.posts.find_one({'link': post['link']}) is None:
            # Let's print it out to verify that we added the new post
            print("Found a new listing at the following url: ", post['link'])
            db_client.bddmongo2.posts.insert(post)
            

