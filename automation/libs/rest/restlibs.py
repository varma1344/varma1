import json
import requests

class Login:
    URL = "api/sign/login"


class RestLibs():
    def __init__(self, cfg = {}):
        self._cfg = cfg
        self._baseurl = self._cfg["url"][:-1] if self._cfg["url"][-1] == "/" else self._cfg["url"]
        self._session = None
        self._token = None
        self._tenant = None
        self._userUuid = None

    def start(self):
        """Starts rest session and login"""
        self._session = requests.Session()
        self.login()

    def login(self, tenantid=None):
        data = {"username":"superadmin@demohospital.com","password":"admin123"}
        if tenantid is not None:
            data["tenant_uuid": tenantid]

        res = self._session.post("%s/%s" % (self._baseurl, Login.URL), data=data)
        if res.status_code not in [200]:
            return False

        ret = res.json()
        if ret["result"] == "LOGIN_SUCCESS":
            resval = ret["response"]
            self._token = resval["accessToken"]
            self._tenant = resval["tenant"]

        return True

    def stop(self):
        """Close web browser"""
        # self._session.
        pass

    def log_info(self, msg):
        print("[INFO]:", self.__class__.__name__, ":", msg)

    def log_error(self, msg):
        print("[ERROR]:", self.__class__.__name__, ":", msg)

    def log_debug(self, msg):
        print("[DEBUG]:", self.__class__.__name__, ":", msg)

    def rest_post(self, url, data, expret = [200]):
        """
        Performance rest api POST operation
        :param url: url (excluding base)
        :param data: Data to send in dict format
        :return: [<True or False>, post response in dict format]
        """
        if self._token is None:
            self.login()

        url = "%s/%s" % (self._baseurl, url)
        hdrs = {"accessToken": self._token, "content-type": "application/json"}
        self._session.headers["accessToken"] = self._token
        self._session.headers["content-type"] = "application/json"
        data = json.dumps(data)
        res = self._session.post(url=url, data=data, headers=hdrs)
        self.log_info("Performed Rest API POST operation:")
        self.log_info("        URL: %s" % url)
        self.log_info("        Data: %s" % data)
        self.log_info("    Response:")
        self.log_info("        code: %s" % res.status_code)
        if res.status_code in [401]:
            self.login()
            self.log_info("Refreshed the token and retry POST")
            res = self._session.post(url=url, header=hdrs, data=data)
            self.log_info("    Response:")
            self.log_info("        code: %s" % res.status_code)

        if res.status_code in expret:
            self.log_debug(res.json())
            self.log_info("        data: %s" % res.text)
            return [True, res.json()]

        self.log_error("        data: %s" % res.text)
        return [False, {}]


    def rest_put(self, url, data, expret = [200]):
        """
        Performance rest api POST operation
        :param url: url (excluding base)
        :param data: Data to send in dict format
        :return: [<True or False>, post response in dict format]
        """
        if self._token is None:
            self.login()

        url = "%s/%s" % (self._baseurl, url)
        hdrs = {"accessToken": self._token, "content-type": "application/json"}
        self._session.headers["accessToken"] = self._token
        self._session.headers["content-type"] = "application/json"
        data = json.dumps(data)
        res = self._session.put(url=url, data=data, headers=hdrs)
        self.log_info("Performed Rest API PUT operation:")
        self.log_info("        URL: %s" % url)
        self.log_info("        Data: %s" % data)
        self.log_info("    Response:")
        self.log_info("        code: %s" % res.status_code)
        if res.status_code in [401]:
            self.login()
            self.log_info("Refreshed the token and retry PUT")
            res = self._session.put(url=url, header=hdrs, data=data)
            self.log_info("    Response:")
            self.log_info("        code: %s" % res.status_code)

        if res.status_code in expret:
            self.log_debug(res.json())
            self.log_info("        data: %s" % res.text)
            return [True, res.json()]

        self.log_error("        data: %s" % res.text)
        return [False, {}]


    def rest_delete(self, url, data, expret = [200]):
        """
        Performance rest api POST operation
        :param url: url (excluding base)
        :param data: Data to send in dict format
        :return: [<True or False>, post response in dict format]
        """
        if self._token is None:
            self.login()

        url = "%s/%s" % (self._baseurl, url)
        hdrs = {"accessToken": self._token, "content-type": "application/json"}
        self._session.headers["accessToken"] = self._token
        self._session.headers["content-type"] = "application/json"
        data = json.dumps(data)
        res = self._session.delete(url=url, data=data, headers=hdrs)
        self.log_info("Performed Rest API DELETE operation:")
        self.log_info("        URL: %s" % url)
        self.log_info("        Data: %s" % data)
        self.log_info("    Response:")
        self.log_info("        code: %s" % res.status_code)
        if res.status_code in [401]:
            self.login()
            self.log_info("Refreshed the token and retry DELETE")
            res = self._session.delete(url=url, header=hdrs, data=data)
            self.log_info("    Response:")
            self.log_info("        code: %s" % res.status_code)

        if res.status_code in expret:
            self.log_debug(res.json())
            self.log_info("        data: %s" % res.text)
            return [True, res.json()]

        self.log_error("        data: %s" % res.text)
        return [False, {}]


    def rest_get(self, url, expret = [200]):
        """
        Performance rest api GET operation
        :param url: url (excluding base)
        :param data: Data to send in dict format
        :return: [<True or False>, post response in dict format]
        """
        if self._token is None:
            self.login()

        url = "%s/%s" % (self._baseurl, url)
        hdrs = {"accessToken": self._token, "content-type": "application/json"}
        self._session.headers["accessToken"] = self._token
        self._session.headers["content-type"] = "application/json"
        res = self._session.get(url=url, headers=hdrs)
        self.log_info("Performed Rest API GET operation:")
        self.log_info("        URL: %s" % url)
        self.log_info("    Response:")
        self.log_info("        code: %s" % res.status_code)

        if res.status_code in [401]:
            self.login()
            self.log_info("Refreshed the token and retry Get")
            res = self._session.get(url=url, header=hdrs)
            self.log_info("    Response:")
            self.log_info("        code: %s" % res.status_code)

        if res.status_code in expret:
            self.log_debug(res.json())
            self.log_info("        data: %s" % res.text)
            return [True, res.json()]

        self.log_error("        data: %s" % res.text)
        return [False, {}]


    from libs.rest._login import login
    from libs.rest._patient import add_patient, get_patient_inventory, _get_patient_inventory, get_patient_by_mrn
    from libs.rest._device import add_device, get_device_inventory, _get_device_inventory, get_device_info
    from libs.rest._association import associate_sensors, get_device_association, detach_sensor

    # Sensor data related libs
    from libs.rest._sensor_data import _form_keepalive_data, _form_alpamed_data, _form_ecg_data, _form_ihealth_data, _form_viatom_data
    from libs.rest._sensor_data import _form_temperature_data, _form_spo2_data, _form_digital_data
    from libs.rest._sensor_data import send_sensor_data

    # Tenant libs
    from libs.rest._tenant import get_all_tenants, get_tenant_id

    # User libs
    from libs.rest._users import get_roles, get_roles_id, add_user


