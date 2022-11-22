import time
from selenium.webdriver.common.by import By

import libs.web.ele_mapping as em

def select_dev_invertory(self):
    """Select device inventory page"""
    try:
        ele = self._webdriver.find_element(em.SideMenu.ROOT[0], em.SideMenu.ROOT[1])
    except:
        time.sleep(3)
        ele = self._webdriver.find_element(em.SideMenu.ROOT[0], em.SideMenu.ROOT[1])

    ele.click()
    # Click on admin only if the menu is not opened
    adminele = self._webdriver.find_element(em.SideMenu.ADMIN[0], em.SideMenu.ADMIN[1])
    adminarrow = self._webdriver.find_element(em.SideMenu.ADMINSUBMENU_SEL[0], em.SideMenu.ADMINSUBMENU_SEL[1])\
                 .find_element(em.SideMenu.ADMINSUBMENU_SEL[2], em.SideMenu.ADMINSUBMENU_SEL[3])

    if em.SideMenu.SUBMEMUCLOSE in adminarrow.get_attribute('style'):
        adminele.click()

    self._webdriver.find_element(em.SideMenu.DEVINVENTORY[0], em.SideMenu.DEVINVENTORY[1]).click()

    return True

def select_add_dev_menu(self):
    """Select Add Device Menu in GUI"""
    self._webdriver.find_element(em.AddDeviceMenu.ADDDEV[0], em.AddDeviceMenu.ADDDEV[1]).click()
    self._webdriver.find_element(em.AddDeviceMenu.DEVICE[0], em.AddDeviceMenu.DEVICE[1]).click()
    return True
