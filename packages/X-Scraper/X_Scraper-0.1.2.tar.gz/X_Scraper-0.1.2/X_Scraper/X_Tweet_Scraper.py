import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By 
class X_Tweet:
    # Initializing the post_link 
    def __init__(self , post_link):
        self.post_link = post_link
        
    def get_X_Tweet(self):
        
         # Boolean to check the link is valid or not 
        bool = True
        try : 
            r = requests.get(self.post_link , timeout=1)
            if r.status_code < 400 : 
                bool = True
            else : 
                bool = False
        except ConnectionError:
            bool = False
        
        # Break the execution if the link is invalid 
        if not bool : 
            print(f"Invalid URL : {self.post_link}")
            return 
        
        # Open the Firefox browser and setting up the driver       
        driver = webdriver.Firefox()

        # Getting the link of the desirable post
        driver.get(self.post_link)

        # Getting the text of the post
        texts = driver.title 

        # Initializing a variable that will help us to differentiate between Author and post
        i = 0 

        # String for getting the author name
        id = " "

        # String for getting the post 
        post = " "

        # Iterating the  text of post which is in actually character array 
        for text in texts:
            # Initializing i value for not taking character to post string
            if text=="X":
                i = 1 
            # i == 0 mean that the characters are part of the author name 
            if i == 0 : 
                id+=text
            # if not then the characters are part of  post and avoid the character X 
            elif i == 1 and text != "X":
                post+=text
                

        # Using re to remove some unnecessary char 
        post = re.sub(r'[":/]' ,'' ,post)
        # Striping post and id string 
        id.strip()

        post.strip()

        # Replacing unncecessary words 
        id = id.rstrip(id[-3:])
        
        driver.quit()
        
        return {
            "Author" : id , 
            "Post" : post 
        }
        
        
        


        
