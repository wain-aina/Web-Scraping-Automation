from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

chrome_driver = "C:\development\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver)

page = driver.get('https://orteil.dashnet.org/cookieclicker/')

cookie = driver.find_element(By.ID, "cookie")
items = driver.find_elements(By.CSS_SELECTOR, "#store div")

upgrades = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
five_min = time.time() + 60*5 # 5minutes

while True:

    cookie.click()

    #check every 5 seconds
    if time.time() > timeout:

        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store .price")
        item_prices = []

        for price in all_prices:
            element = price.text
            if element != "":
                cost = int(element.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        #create dictionarry of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = upgrades[n]

        money_element = driver.find_element(By.ID, "money").text
        if "," in money_element:
            money_element = money_element.replace(",", '')
        cookie_count = int(money_element)

        #find items we can afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        #purchase the most expensive affordable upgrade
        highest_price_affordable = max(affordable_upgrades)
        to_purchase_id = affordable_upgrades[highest_price_affordable]

        driver.find_element(By.ID, to_purchase_id).click()

        timeout = time.time() + 5

    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.ID, "cps").text
        break

