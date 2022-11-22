from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
url = "http://20.83.211.88:7141/"

driver.get(url)
assert "Live247" in driver.title
elem = driver.find_element("id", "username")
elem.clear()
elem.send_keys("superadmin@demohospital.com")
elem = driver.find_element("id", "password")
elem.clear()
elem.send_keys("admin123")
elem = driver.find_element(By.XPATH, '//button[@type="submit"]')
elem.click()
LOGIN_WAIT_ON = "//h3[contains(text(),'Patient Type:')]"
elem = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, LOGIN_WAIT_ON)))
#elem = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//h3")))


print(elem)
driver.close()

