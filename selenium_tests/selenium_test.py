import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

APP_URL = "http://webapp:5000"

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    return driver

def test_home_page_title():
    driver = get_driver()
    driver.get(APP_URL)
    time.sleep(2)

    heading = driver.find_element(By.TAG_NAME, "h1").text
    assert "Simple User Management App" in heading

    driver.quit()

def test_add_user_form():
    driver = get_driver()
    driver.get(APP_URL)
    time.sleep(2)

    input_box = driver.find_element(By.NAME, "name")
    input_box.send_keys("Ahmed")

    button = driver.find_element(By.TAG_NAME, "button")
    button.click()

    time.sleep(2)

    page_source = driver.page_source
    assert "Ahmed" in page_source

    driver.quit()