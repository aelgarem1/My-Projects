
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from urllib.parse import quote_plus
from random import choice
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
USERNAME = "AmiAli597314"
PASSWORD = "DS4082024"

service = Service(log_output="geckodriver.exe") 
user ='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0/jM08djK0yDS8Zq-81'
firefox_profile = webdriver.FirefoxOptions()
firefox_profile.set_preference('general.useragent.override', user)
driver = webdriver.Firefox(service=service)
jumia_base_url = 'https://www.jumia.com.eg/'  
driver.get(jumia_base_url)

try:
    close_popup = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="newsletter_popup_close-cta"]')
    close_popup.click()
    #close_popup = driver.find_element(By.CSS_SELECTOR, '[button.btn:nth-child(3)]')
    #close_popup.click()
except:
    print("No popup detected!")

phones_url =  driver.find_element(By.CSS_SELECTOR,'div.sub:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)').get_attribute('href')
tablets_url = driver.find_element(By.CSS_SELECTOR, 'div.sub:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)').get_attribute('href')
categories = [phones_url, tablets_url]
title_list = []
price_list = []
url_list = []
old_price_list = []
discount_percent = []
for category in categories:
    driver.get(category)
    #for page in range(1,2):
        #page_url = category + '?page=' + str(page) + '#catalog-listing'
        #driver.get(page_url)
        #products = driver.find_elements(By.CLASS_NAME, '-paxs.row._no-g._4cl-3cm-shs article.prd._fb.col.c-prd')
    title = driver.find_elements(By.CLASS_NAME, "name")
    price = driver.find_elements(By.CLASS_NAME,"prc")
    url = driver.find_elements(By.CLASS_NAME, "core")
    old_price = tuple(driver.find_elements(By.CLASS_NAME, 's-prc-w'))
    discount =  tuple(driver.find_elements(By.CLASS_NAME, 's-prc-w'))
    Num_Groups = len(old_price)
    #products_info = []

    try:
        for i in range(Num_Groups):
            
            title_list.append(title[i].text)
            price_list.append(price[i].text)
            url_list.append(url[i].get_attribute('href'))
            old_price_list.append(old_price[i].text.split()[1])
            discount_percent.append(discount[i].text.split()[2])

    except:
            continue

df = pd.DataFrame({
        'title': title_list,
        'current_price': price_list,
        'url': url_list,
        'old_price': old_price_list,
        'discount' : discount_percent,
        'published_at': False 
    })


df['current_price'] = df['current_price'].str.strip('EGP').str.replace(',', '').astype(float)

df['discount'] = df['discount'].str.strip('%')

df['old_price'] = df['old_price'].str.replace(',', '').astype(float)

df['discount'] = df['discount'].astype(int)

df.to_csv('jumia_sale.csv')


driver.get("https://x.com/login")
wait = WebDriverWait(driver, 10)

# Enter username
username_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
username_field.send_keys(USERNAME)
username_field.send_keys(Keys.RETURN)

# Enter password
sleep(2)  # Adjust sleep if necessary to account for page load
password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
password_field.send_keys(PASSWORD)
password_field.send_keys(Keys.RETURN)

# Wait for login to complete
sleep(5)

tweet_box = driver.find_element(By.CSS_SELECTOR, '.public-DraftStyleDefault-block')
tweet_box.click()

top_discounts = df.nlargest(5, "discount")[["title", "current_price", "old_price", "discount"]]

# Tweet templates
tweet_templates = [
"🚀 Amazing discounts on Jumia right now! 🎉 Check out our top deals:\n{products}\nDon’t miss out! 🛒 #JumiaDeals #BigSavings",
"⏳ Limited-Time Offer Alert!\nGrab the hottest discounts on Jumia:\n{products}\nHurry, deals are selling out fast! 🛍️ #ShopNow #HotDeals 🚨",
"💎 Exclusive Savings Just for You! 💎\n{products}\nGrab it now before it’s gone! #JumiaSales",
"🎄 Holiday Sale Alert! 🎁\n🎉 Celebrate the season with these top deals:\n{products}\nShop now and spread the joy! 🌟 #JumiaDeals #HolidaySavings",
"🌟 Premium Deals on Jumia! 🌟\nIndulge in luxury at discounted prices:\n{products}\nUpgrade your style today! 💼✨ #LuxurySavings",
"💬 What are you shopping for today?\nCheck out these epic Jumia discounts:\n{products}\nComment below your favorite deal! 🔥🛒 #ShopWithUs #JumiaDeals",
"🔥 Trending on Jumia! 🔥\nTop-selling items at unbeatable discounts:\n{products}\nGet yours before the trend ends! 🎮🛍️ #JumiaHotPicks"
]

# Format top-discounted products into a string
formatted_products = ""
for idx, row in top_discounts.iterrows():
    formatted_products += f"- {row['title']}:\n   Old Price: {row['old_price']} EGP\n   Now: {row['current_price']} EGP (-{row['discount']}%)"

    # Select a random template
    random_template = choice(tweet_templates)

    # Insert the product details into the template
    tweet_message = random_template.format(products=formatted_products)
    tweet_box = driver.find_element(By.CSS_SELECTOR, '.public-DraftStyleDefault-block')
    tweet_box.click()   
    driver.execute_script("document.querySelector('div.r-17gur6a').textContent = arguments[0]", tweet_message)
    post_box = driver.find_element(By.CSS_SELECTOR, 'button.r-1cwvpvk > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)')
    post_box.click()
    current_time = datetime.now()
    df.loc[top_discounts.index, "published_at"] = current_time 
    break



