import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

link = f"https://tunebat.com/analyzer"
job_link = link
driver.get(job_link)

while True:
    try:
        cookie_button = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div[2]/div[1]/button[3]/span")
        cookie_button.click()
        break
    except Exception as e:
        print(e)
        time.sleep(2)
