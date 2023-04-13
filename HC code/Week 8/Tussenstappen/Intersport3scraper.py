import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from subprocess import Popen
from msedge.selenium_tools import Edge, EdgeOptions
import csv

#schrijf de header naar het bestand
fieldnames = ['product', 'reviews', 'img']
product_data = []

#open browser
driver = webdriver.Edge()

#visit site
driver.get("https://www.intersport.nl/search?q=wandelschoenen&lang=nl_NL&page=15")

assert "Intersport" in driver.title

time.sleep(5)
driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

isDone = True
scrollOnce = 0
productLinkList = []

while isDone:
    nextPageButton = driver.find_element(By.CLASS_NAME, "js-loadmore")
    if scrollOnce == 1:
        allPageButton = driver.find_element(By.CLASS_NAME, "js-loadall")
        driver.execute_script("arguments[0].scrollIntoView(true);", allPageButton)
        time.sleep(.5)
        driver.execute_script("window.scrollBy(0, -250);")
        allPageButton.click()
        scrollOnce = 2
    if (nextPageButton.value_of_css_property("display") != "none") & (scrollOnce == 0):
        driver.execute_script("arguments[0].scrollIntoView(true);", nextPageButton)
        time.sleep(.5)
        driver.execute_script("window.scrollBy(0, -250);")
        nextPageButton.click()
        scrollOnce = 1

    if scrollOnce == 2:
        productLinkList = []
        # get all products
        productList = driver.find_elements(By.CLASS_NAME, "js-product-tile")
        # collect all links and save them
    for product in productList:
        productId = product.get_attribute("data-tracking-productdata")
        d = json.loads(productId)
        link = product.find_element(By.CLASS_NAME, "name-link")
        productLinkList.append([d["id"], link.get_attribute("href")])

    isDone = False

time.sleep(3)
apiParams = []
r = 0
count = 0

for product in productLinkList:
    try:
        driver.get(product[1])
        time.sleep(.5)
        stepTotalReview = driver.find_element(By.CLASS_NAME, "bv-content-product-stats-item-reviews")
        totalReview = stepTotalReview.find_element(By.CLASS_NAME, "bv-content-title")
        reviewObject = driver.find_element(By.ID, "bv-jsonld-reviews-data").get_attribute("innerHTML")
        data = json.loads(reviewObject)
        reviewCombined = ""
        pictureObject = driver.find_element(By.CLASS_NAME, "picture-tag")
        imgObject = pictureObject.find_element(By.TAG_NAME, "img")
        img = imgObject.get_attribute("src")

        for review in data['review']:
            reviewCombined = review['headline'] + ":" + review['reviewBody']
            if len(reviewCombined.split()) > 69:
                product_data.append({"product": product[0], "reviews": reviewCombined.replace('\n', ''), "img": img})
                r += 1
            else:
                product_data.append({"product": product[0], "reviews": "TO SHORT", "img": img})
        time.sleep(.5)

    except:
        pictureObject = driver.find_element(By.CLASS_NAME, "picture-tag")
        imgObject = pictureObject.find_element(By.TAG_NAME, "img")
        img = imgObject.get_attribute("src")
        product_data.append({'product': product[0], 'reviews': [], 'img': img})
    print("[" + str(count) + "/411]")
    int(count)
    count += 1
print(r)
driver.quit()





