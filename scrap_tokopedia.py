from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

url = "https://www.tokopedia.com/msi-id/review"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.get(url)

data = []

for i in range(0, 5):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    containers = soup.findAll('article', class_='css-1pr2lii')

    for container in containers:
        try:
            review = container.find('span', attrs={'data-testid': 'lblItemUlasan'}).text 
            data.append(
                (review)
            )
        except AttributeError:
            continue 

time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "button[aria-label ^='Laman berikutnya']" ).click()
time.sleep(3)

df = pd.DataFrame(data, columns=['Review'])
df.to_csv('msi_reviews.csv', index=False, encoding='utf-8-sig')
driver.quit()