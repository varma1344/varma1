from cmath import exp
import json
import math

class Patient:
    INVENTORY = "api/patientinventory"
    PATIENT = "api/patients"

def _get_patient_inventory(self, type="remote", offset=1, limit=100):
    data =  {"tenantId": self._tenant,
            "patientType": type,
            "EWS": [0, 20],
            "spo2LevelsL": [0, 100],
            "respirationRate": [0, 100],
            "offset": offset, "limit": limit,
            "duration": 10}

    status,retval = self.rest_post(url=Patient.INVENTORY, data=data)
    if not status or retval["result"] not in ["FETCH_PATIENT_INVENTORY_SUCCESS"]:
        return False,{}

    return status, retval["response"]

def get_patient_by_mrn(self, mrn, loc, offset=1, limit=1, alldet=False):
    data =  {"tenantId": self._tenant, "patientType": loc, "offset": offset, "limit": limit, "name": mrn}

    status,retval = self.rest_post(url=Patient.INVENTORY, data=data)
    if not status or retval["result"] not in ["FETCH_PATIENT_INVENTORY_SUCCESS"]:
        return 0,{}

    if alldet:
        return len(retval["response"]["patients"]),retval["response"]["patients"][0]

    return len(retval["response"]["patients"]), retval["response"]["patients"][0]["demographic_map"]


def get_patient_inventory(self,  type="remote"):
    """
    Get Patient inventory data.
    :return: [<True or False>, Data in dict format]
    """
    if self._tenant is None: self.start()

    retdata = {}
    maxofset = 1
    offset = 1
    limit = 500
    while offset <= maxofset:
        status,retval = self._get_patient_inventory(type=type, offset=offset, limit=limit)
        if offset == 1:
            pcnt = retval["patientTotalCount"]
            maxofset = math.ceil(pcnt/limit)

        if not status:
            print("Failed to patient inventory")
            return retdata

        for dev in retval["patients"]:
            retdata[dev["demographic_map"]["med_record"]] = dev

        offset += 1

    return retdata


def get_patient_details(self, explist):
    """
    Get Patient Details
    :param lname: Last name
    :param fname: First name
    :param mrn: Medical Record
    :param dob: Date of Birth
    :return: Patient data list or []
    """
    if self._tenant is None: self.start()

    patients = self.get_patient_inventory()
    retlist = []
    keys = patients.keys()
    keys.sort()
    for k in keys:
        p = patients[k]
        if p["demographic_map"]["lname"].lower() == explist["lname"] and \
                p["demographic_map"]["fname"].lower() == explist["fname"] and \
                p["demographic_map"]["med_record"].lower() == explist["med_record"] and \
                p["demographic_map"]["DOB"].lower() == explist["DOB"]:
            retlist.append(p)

    return retlist


def add_patient(self, indata):
    """
    Add Patient.
    :return: <True or False>
    """
    if self._tenant is None: self.start()

    data = {
        "tenantId": self._tenant,
        "demographic_map": {
            "admission_date": indata["admission_date"],
            "title": indata["title"], "fname": indata["fname"], "mname": indata["mname"], "lname": indata["lname"],
            "med_record": indata["med_record"],
            "country_name": indata["country_name"] if "country_name" in indata else "United States",
            "sex": indata["sex"], "DOB": indata["DOB"], "phone_contact": indata["phone_contact"],
            "tenant_id": self._tenant, "status": "active", "patient_type": indata["patient_type"],
            "email": indata["email"]
        }
    }
    self.log_info("Add patient: %s" % json.dumps(data))
    status, retdata = self.rest_post(Patient.PATIENT, data=data, expret = [200, 470])
    if not status: return False
    return True if retdata["Code"] in ["CREATE_PATIENT_SUCCESS", "MED_RECORD NUMBER ALREADY EXISTS"] else False


def del_patients(self, plist):
    """
    Delete Patients.
    :return: <True or False>
    """
    pdatalist = self.get_patient_details(explist=plist)
    pidlist = [{"pid": p["pid"]} for p in pdatalist]
    data = {"tenantId": self._tenant, "list": pidlist}
    self.log_info("Delete patients {}".format(data))
    status, retdata = self.rest_delete(Patient.PATIENT, data=data)
    if retdata["result"] in ["DELETE_PATIENT_SUCCESS"]:
        return True

    return False


if __name__ == "__main__":
    import libs.rest.restlibs as restlibs

    test = {"url": "http://us.livehealthyvibes.com:7124", "username": "testtenant06@live247.com", "password": "admin123"}
    robj = restlibs.RestLibs(cfg = test)
    robj.get_patient_inventory({
            "admission_date": "2022-11-01",
            "title": "Mr.", "fname": "SPAT0004", "mname": "spat", "lname": "Tsttenant0604",
            "med_record": "SMRN00007",
            "sex": "male", "DOB": "2000-05-18", "phone_contact": "16030000007"
        })
    print(robj.get_patient_inventory())
    plist = [{
            "fname": "SPAT0004", "mname": "spat", "lname": "Tsttenant0604",
            "med_record": "SMRN00007", "DOB": "2000-05-18"
        }]
    if len(robj.get_patient_details(plist)) == len(plist):
        print("Patient Found")
        robj.del_patients(plist)
