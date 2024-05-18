from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from time import sleep
import csv

service = Service('/usr/local/bin/chromedriver')
chrome_options = Options()
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://steamdb.info/sales/"
driver.get(url)
wait = WebDriverWait(driver, 10)

try:
    select = Select(wait.until(EC.presence_of_element_located((By.ID, 'dt-length-0'))))
    select.select_by_value('-1')  # Selecionar tudo "All"

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'tr.app')))
    sleep(5) 

    scroll_pause_time = 1 #Sleep para pegar o 'end' e 'start'
    screen_height = driver.execute_script("return window.innerHeight")
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        for i in range(1, int(last_height/screen_height) + 1):
            driver.execute_script(f"window.scrollTo(0, {i * screen_height});")
            sleep(scroll_pause_time)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    games = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.app')))
    
    print(f'Encontrados: {len(games)}')

    with open('steam_raspagem.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Discount', 'Price', 'Rating', 'Release', 'Ends', 'Started'])

        for game in games:
            details = game.find_elements(By.CSS_SELECTOR, 'td')
            if len(details) >= 9:
                name = details[2].find_element(By.TAG_NAME, 'a').text
                discount = details[3].text
                price = details[4].text
                rating = details[5].text
                release_date = details[6].text
                ends = details[7].get_attribute('title').split(' at ')[0]
                starts = details[8].get_attribute('title').split(' at ')[0]
                
                writer.writerow([name, discount, price, rating, release_date, ends, starts])

except Exception as e:
    print("Erro:", e)
finally:
    driver.quit()
