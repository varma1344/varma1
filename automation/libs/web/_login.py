from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import libs.web.ele_mapping as em

def login(self):
    url = self._cfg["url"]
    self._webdriver.get(url)
    if "Live247" not in self._webdriver.title:
        return False

    elem = self._webdriver.find_element(em.Login.USER[0], em.Login.USER[1])
    elem.clear()
    elem.send_keys(self._cfg["username"])
    elem = self._webdriver.find_element(em.Login.PASSWORD[0], em.Login.PASSWORD[1])
    elem.clear()
    elem.send_keys(self._cfg["password"])

    elem = self._webdriver.find_element(em.Login.SUBMIT[0], em.Login.SUBMIT[1])
    elem.click()

    if "Live247" not in self._webdriver.title:
        return False

    self.log_info("Wait till device inventory is loaded")
    WebDriverWait(self._webdriver, 120).until(
        EC.presence_of_element_located((em.Login.LOGIN_WAIT_ON[0],em.Login.LOGIN_WAIT_ON[1])))
    return True
