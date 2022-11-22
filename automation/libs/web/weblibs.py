from selenium import webdriver

class WebLibs():
    def __init__(self, cfg={}):
        self._cfg = cfg
        self._webdriver = None
        self.browser = "firefox"

    def start_web(self):
        """Starts web browser"""
        if self.browser == "firefox":
            self._webdriver = webdriver.Firefox()

    def stop_web(self):
        """Close web browser"""
        #self._webdriver.close()
        pass

    def log_info(self, msg):
        print("[INFO]:", self.__class__.__name__, ":", msg)

    def log_error(self, msg):
        print("[ERROR]:", self.__class__.__name__, ":", msg)

    def log_debug(self, msg):
        print("[DEBUG]:", self.__class__.__name__, ":", msg)

    from libs.web._device import add_device, delete_device
    from libs.web._menu import select_dev_invertory, select_add_dev_menu
    from libs.web._login import login

