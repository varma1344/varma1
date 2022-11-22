import json
import time
import requests

class Login:
    LOGIN = "api/sign/login"

def login(self, tenantid=None):
    """Login to live247"""
    url = "%s/%s" % (self._baseurl, Login.LOGIN)
    data = {"username": self._cfg["username"],"password": self._cfg["password"]}
    if tenantid is not None:
        data["tenant_uuid"] = tenantid

    self._session = requests.Session()
    hdrs = {"Content-Type": "application/json"}
    for i in range(0, 3):
        res = self._session.post(url=url, data=json.dumps(data), timeout=180, headers=hdrs)
        if res.status_code in [200]:
            self.log_info("Successfully authenticated rest api service")
            resdata = res.json()
            if resdata["result"] == "LOGIN_SUCCESS":
                self._token = resdata["response"]["accessToken"]
                self._tenant = resdata["response"]["tenant"]
                return True

            time.sleep(5)

    self.log_error("Failed to authenticate rest api service")
    return False
