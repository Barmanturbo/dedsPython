import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

response = requests.get("https://www.decathlon.nl/search?Ntt=outdoor%20schoenen")


soup = BeautifulSoup(response.content, "html.parser")

producten = soup.find_all("div", {"class": "product-block-top-main vtmn-flex vtmn-flex-col vtmn-items-center"})

reviews = []

waardering = []
productid = []
wordcount = []