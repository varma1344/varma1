from cmath import exp
import json
import math

class Users:
    INVENTORY = "api/patientinventory"
    USERS = "api/users"
    ROLE = "api/role/select-box"


def get_roles(self):
    """Get User roles"""
    status,retval = self.rest_get(url=Users.ROLE)
    if not status or retval["Code"] not in ["FETCH_ROLE_INVENTORY_SUCCESS"]:
        return False,{}

    return True, retval["response"]["data"]

def get_roles_id(self, name):
    """Get User roles"""
    status, roles = self.get_roles()
    if status:
        for role in roles:
            if role["role_name"].lower() == name.lower():
                return role["role_uuid"]
    return None


def add_user(self, indata, tenant_id, role_uuid):
    """
    Add user.
    :return: <True or False>
    """
    if self._tenant is None: self.start()

    data = {
        "title": indata["title"], "fname": indata["fname"], "lname": indata["lname"],
        "username": indata["username"], "password": indata["password"],
         "role_uuid": role_uuid, "tenant_id": tenant_id,
         "phone": indata["phone"], "email": indata["email"]
    }
    self.log_info("Add user under tenant %s : %s" % (tenant_id, json.dumps(data)))
    status, retdata = self.rest_post(Users.USERS, data=data, expret = [200, 470])

    if not status:
        return False

    if retdata["Code"] in ["CREATE_PATIENT_SUCCESS", "MED_RECORD NUMBER ALREADY EXISTS"]:
        return True

    return False


if __name__ == "__main__":
    import libs.rest.restlibs as restlibs

    test = {"url": "http://40.112.217.42:7124/", "username": "scaladmin001@demohospital.com", "password": "admin123"}
    robj = restlibs.RestLibs(cfg = test)
    robj.add_patient({
            "admission_date": "2022-11-01",
            "title": "Mr.", "fname": "APFname001", "mname": "ApM001", "lname": "APLname001",
            "med_record": "AutoTestPatient001",
            "sex": "male", "DOB": "1960-10-21", "phone_contact": "16030000007"
        })
    print(robj.get_patient_inventory())
    plist = [{
            "fname": "APFname001", "mname": "ApM001", "lname": "APLname001",
            "med_record": "AutoTestPatient001", "DOB": "1960-10-21"
        }]
    if len(robj.get_patient_details(plist)) == len(plist):
        print("Patient Found")
        robj.del_patients(plist)
