import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

import libs.web.ele_mapping as em

def add_device(self, serial, type, details):
    """
    Add device to inventory.
    :param serial: Device Serial Number
    :param type: Device Type. Support Values same as in Web UI
    :param details: Device details like in dict format:
                     {"macaddress": "Mac Address"}
    :return: True or False
    """
    status = self.select_dev_invertory()
    status &= self.select_add_dev_menu()

    # Select Type
    driver = self._webdriver
    driver.find_element(em.AddDeviceModal.TYPE[0], em.AddDeviceModal.TYPE[1]).click()
    driver.find_element(em.AddDeviceModal.TYPE[2], em.AddDeviceModal.TYPE[3]).\
        find_element(em.AddDeviceModal.TYPE[4], em.AddDeviceModal.TYPE[5] % type).click()

    # Set Serial Number
    ele = driver.find_element(em.AddDeviceModal.SERIAL[0], em.AddDeviceModal.SERIAL[1])
    ele.clear()
    ele.send_keys(serial)

    # Set Mac address
    ele = driver.find_element(em.AddDeviceModal.MACADDR[0], em.AddDeviceModal.MACADDR[1])
    ele.clear()
    ele.send_keys(details["macaddress"])

    # Click Add device button
    element = driver.find_element(em.AddDeviceModal.ADDBUTTON[0], em.AddDeviceModal.ADDBUTTON[1])\
                     .find_element(em.AddDeviceModal.ADDBUTTON[2], em.AddDeviceModal.ADDBUTTON[3])
    element.click()

    # Close the dialog
    #FIX-L: Repalce hard timeout with a logic to poll an element
    try:
        driver.find_element(em.AddDeviceModal.CLOSE[0], em.AddDeviceModal.CLOSE[1]).click()
    except:
        time.sleep(3)
        driver.find_element(em.AddDeviceModal.CLOSE[0], em.AddDeviceModal.CLOSE[1]).click()
        time.sleep(1)

    return status

def delete_device(self, serial, type):
    """
    Delete Device from Inventory

    :param serial: Device Serial Number
    :param type: Device Type. Support Values same as in Web UI
    :return: True or False
    """
    return True
