from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

url = "https://play.google.com/store/apps/details?id=com.shopee.id&hl=id"

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get(url)
data = []

try:
    see_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Lihat semua ulasan']]"))
    )
    see_all_button.click()
    print("Tombol 'See all reviews' berhasil diklik.")

except Exception as e:
    print("Gagal klik tombol:", e)
    driver.quit()
    exit()

time.sleep(3)

scrollable_div = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[jsname="bN97Pc"]'))
)

scroll_count = 200

for i in range(scroll_count):
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
    print(f"Scroll ke-{i+1} di dalam pop-up")
    time.sleep(1)

soup = BeautifulSoup(driver.page_source, 'html.parser')
containers = soup.findAll('div', class_='RHo1pe')

for container in containers:
    try:
        review = container.find('div', attrs={'class': 'h3YV2d'}).text 
    
        rating_div = container.find('div', class_='iXRFPc')
        rating_text = rating_div['aria-label'] 
        rating = int(rating_text.split(' ')[2])

        date_span = container.find('span', class_='bp9Aid')
        review_date = date_span.text.strip()

        data.append((review_date, rating, review))

    except AttributeError:
        continue 

time.sleep(3)

print(len(data), "reviews collected.")
df = pd.DataFrame(data, columns=['Date', 'Rating', 'Review'])
df.to_csv('shopee_reviews.csv', index=False, encoding='utf-8-sig')
driver.quit()

