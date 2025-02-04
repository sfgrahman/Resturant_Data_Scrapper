import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from random import randint
import pandas as pd
import re
#city = str(input('type the destination city: '))
#page_no = int(input('how many page do you scrap: '))

base_url = f'https://www.yelp.com/search?cflt=restaurants&find_loc=New+York%2C+NY'
final_processed_data = {}
j=0
for i in range(0,10):
    print(i)
    if i==0:
        topic_url = base_url
    else:
        topic_url = base_url+"&start="+str((i)*10)
    print(topic_url)
    options = webdriver.EdgeOptions()
    options.add_argument(f"--app={topic_url}")
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation"]
    )
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--inprivate")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--ignore-certificate-errors")

    driver = webdriver.Edge(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    driver.maximize_window()
    driver.get(topic_url)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    super_tags = soup.find("ul", class_="list__09f24__ynIEd")
    list_items = super_tags.find_all("li", recursive=False)
    start_index = 7 
    end_index = 16  
    selected_items = list_items[start_index:end_index+1]
    for s in selected_items:
        restaurant_list = {}
        try:
            restaurant_name = s.find("a", class_="y-css-1x1e1r2").text
        except:
            restaurant_name=""
        restaurant_list["Restaurant name"] = restaurant_name
        try:
            rating = s.find("span", class_="y-css-1ugd8yy").text
        except:
            rating = ""
        restaurant_list["Rating"] = rating
        try:
            num_reviews = s.find("span", class_="y-css-1d8mpv1").text
            number = num_reviews.replace("(", "").replace(" reviews)", "")
            #number = re.sub(r"\D", "", num_reviews)
        except:
            number=""
        restaurant_list["Reviews"] = number
        try:
            location = s.find("span", class_="y-css-4p5f5z").text
        except:
            location=""
        restaurant_list["Location"] = location
        try:
            cuisine_tag = s.find_all("p", class_ ="y-css-1iketvw")
            cuisine = [link.text for link in cuisine_tag]
            formatted_cuisine_list = ', '.join(cuisine)
        except:
            formatted_cuisine_list =""
        
        restaurant_list["Cuisine"] = formatted_cuisine_list
        try:
            yelp_link = s.find("a", class_="y-css-1x1e1r2").get("href")
            yelp_link_complete = f"https://www.yelp.com{yelp_link}"
        except:
            yelp_link_complete=""
        restaurant_list["Yelp Link"] = yelp_link_complete
        j += 1
        final_processed_data[j] = restaurant_list
    driver.quit()
    
df = pd.DataFrame.from_dict(final_processed_data, orient="index")
df.to_csv("newyork_restaurents.csv", index=False)

    