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

base_url = "https://www.opentable.com/lolz-view-all/H4sIAAAAAAAA_6tWMlKyUjIyMDLVNTDSNbAMMTS1MjG3MjBQ0lEyRpEBCpgABQwNgZIQeVMlKyMdJTOgoImBnrmhkbm5hY6uuYmegYGZoaEhUIEFUCrANSjY38_RxzPKNSg-MNQ1KBIoYQmUUPYvLUnJzy9yyczLzEsHChoC7YuOBdJAa9ISc4pTawG4fqr9nQAAAA==?originid=e2872cd4-b6a5-4d7c-865a-d0f5211d67f8"

options = webdriver.EdgeOptions()
options.add_argument(f"--app={base_url}")
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
driver.get(base_url)
time.sleep(10)
soup = BeautifulSoup(driver.page_source, "html.parser")
elements = soup.find_all(attrs={"data-marketing-ids": True})
final_processed_data = {}
j = 0 
for el in elements:
    restaurant_list = {}
    restaurant_name = el.find("h6", class_="FhfgYo4tTD0-").text
    formatted_text_name = re.sub(r'^\d+\.\s*', '',  restaurant_name)
    restaurant_list["Restaurant name"] = formatted_text_name
    
    star_rating = el.find("div", class_="tSiVMQB9es0-").text
    restaurant_list["Star Rating"] = star_rating
    
    star_text = el.find("span", class_="MLhGCA4nv6o-").text
    restaurant_list["Star Text"] = star_text
    
    review = el.find("a", class_="XmafYPXEv24-").text
    number = review.replace("(", "").replace(")","")
    restaurant_list["Number of Review"] =  number
    
    price = el.find("span", class_="Vk-xtpOrXcE-").text
    price_f = price.replace("Price: ", "")
    restaurant_list["Price"] = price_f
    
    cuisine_location  = el.find("div", class_="_4QF0cXfwR9Q-").text
    formatted_text = cuisine_location.replace("•", "").strip().replace("  ", ", ")
    restaurant_list["Cuisine"]=formatted_text
    
    booked_today = el.find("span", class_="gr6nnXdRSXE- IGV93qnDV0o- ZwYsiyOew-Q- NeZOcLtuYGk-").text
    restaurant_list["Booked Today"]=booked_today
    
    read_text = el.find("span", class_="l9bbXUdC9v0- _3YSslEmZu4g- C7Tp-bANpE4- l-AMWW5ZrIg-").text
    restaurant_list["Extra Text"]=read_text
    
    opentable_url = el.find("a", class_="qCITanV81-Y-")['href']
    restaurant_list["Opentable URL"] = opentable_url
    j += 1
    final_processed_data[j] = restaurant_list

df = pd.DataFrame.from_dict(final_processed_data, orient="index")
df.to_csv("opentable_demo_restaurents.csv", index=False)
driver.close()