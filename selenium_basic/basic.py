from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from shutil import which
import time
options = Options()
#options.add_argument("--headless")

chrome_path = which("chromedriver")

driver = webdriver.Chrome(executable_path=chrome_path,chrome_options=options)#Options=chrome_options)
driver.get("https://duckduckgo.com")

search_input = driver.find_element_by_id("search_form_input_homepage")
search_input.send_keys("My User Agent")

# search_btn = driver.find_element_by_id("search_button_homepage")
# search_btn.click()

search_input.send_keys(Keys.ENTER)
print(driver.page_source)
time.sleep(300)
driver.close()