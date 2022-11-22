from selenium.webdriver.common.by import By

class Login:
    LOGIN_WAIT_ON = [By.XPATH, "//h3[contains(text(),'Patient Type:')]"]
    USER = [By.ID, "username"]
    PASSWORD = [By.ID, "password"]
    SUBMIT = [By.XPATH, '//button[@type="submit"]']

class SideMenu:
    ROOT = [By.CSS_SELECTOR, ".anticon-menu-unfold > svg"]
    SUBMEMUCLOSE = "rotate(90deg)"
    ADMIN = [By.XPATH, "//span[contains(text(),'Admin')]"]
    ADMINSUBMENU_SEL = [By.XPATH, "//span[contains(text(),'Admin')]/following-sibling::span", By.TAG_NAME, "svg"]
    DEVINVENTORY = [By.CSS_SELECTOR, "li:nth-child(2) .submenu-list:nth-child(1) > li"]
    DEVINVENTORY_TEXT = [By.XPATH, "//a[@href='/dashboard/patchInventory']"]

class AddDeviceMenu:
    ADDDEV = [By.CSS_SELECTOR, ".ant-btn > span:nth-child(3)"]
    DEVICE = [By.CSS_SELECTOR, ".ant-dropdown-menu-title-content"]

class AddDeviceModal:
    CLOSE = [By.XPATH, "//button[@class='ant-modal-close']"]
    TYPE = [By.CSS_SELECTOR, ".ant-select-in-form-item .ant-select-selection-item",
            By.CSS_SELECTOR, ".ant-select-item-option-active",
            By.XPATH,"//div[contains(text(), '%s')]"]
    SERIAL = [By.ID, "basic_serialNumber"]
    MACADDR = [By.ID, "basic_macAddress"]
    ADDBUTTON = [By.CSS_SELECTOR, ".ant-form-item-control-input-content > .ant-btn",
                 By.XPATH, "span[contains(text(), 'Add Device')]"]