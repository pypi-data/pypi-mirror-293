import time 
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
from requests.exceptions import ConnectionError
import requests
from tqdm import tqdm



class X_Image:
    
    # init 
    
    def __init__(self , pic_link):
        self.pic_link = pic_link
    
    def get_X_Image(self):
        # Boolean to check the link is valid or not 
        bool = True
        try : 
            r = requests.get(self.pic_link , timeout=1)
            if r.status_code < 400 : 
                bool = True
            else : 
                bool = False
        except ConnectionError:
            bool = False
        
        # Break the execution if the link is invalid 
        if not bool : 
            print(f"Invalid URL : {self.pic_link}")
            return 

        
        # file savename 
        picture_filename = 'x_picture2.jpg'

        # open firefox browser 
        driver = webdriver.Firefox()

        # open url 
        driver.get(self.pic_link)

        # wati enough time 
        time.sleep(10)

        # Using beautifulsoup to find the image 

        soup = BeautifulSoup(driver.page_source , features="lxml")
        images = soup.find_all('img')

        images = [img['src'] for img in images if '/media/' in img['src']]

        for image in tqdm(images, desc="Downloading images"):
             urllib.request.urlretrieve(image, picture_filename)
        
        # Closing the browser
        driver.quit()

    


