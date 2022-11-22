import datetime
import json
import math
import random

def associate_sensors(self, patient, sensors, gateway, alldlist=None, allplist=None, backdays=0, dryrun=False):
    print("Associating sensor using rest api....")
    print(patient)
    print(sensors)

    if self._tenant is None: self.start()

    pid = patient["pid"] if allplist is None else allplist[patient["med_record"]]["demographic_map"]["pid"]
    sts = datetime.datetime.now() - datetime.timedelta(days=backdays) - datetime.timedelta(days=random.randint(1, 3))
    ets = datetime.datetime.now() + datetime.timedelta(days=random.randint(30, 90))
    sdate = "%s-%02d-%02d" % (sts.year, sts.month, sts.day)
    edate = "%s-%02d-%02d" % (ets.year, ets.month, ets.day)

    currlist = []
    patchlist = []
    for s in sensors + [gateway]:
        patchuuid = s["patch_uuid"] if alldlist is None else alldlist[s["device_serial"]]["patch_uuid"]
        type = s["patch_type"]
        currlist.append(type)
        sdata = {
            "patch_uuid": patchuuid,
            "%s_patch_serial" % type: s["device_serial"],
            "type_device": type,
            "%s_duration" % type: ["%sTZ00:00:00" % sdate, "%sTZ23:59:59" % edate],
            "duration": "%s,%s" % (sdate, edate),
            "config": {}
        }
        patchlist.append(sdata)

    data = {
        "tenantId": self._tenant,
        "pid": pid,
        "associated_list": currlist,
        "list": patchlist
    }

    self.log_info("Associate Devices: %s" % json.dumps(data))
    url = "api/patients/%s/patch_map" % pid
    if dryrun:
        return True
    status, retdata = self.rest_post(url, data=data, expret = [200])
    if not status: return False
    return True if retdata["Code"] in ["CREATE_PATCH_SUCCESS"] else False

def get_device_association(self, patient):
    if self._tenant is None: self.start()
    url = "api/patients/%s/patch_map?limit=100&offset=10&filter=0&tenantId=%s" % (patient, self._tenant)
    self.log_info("Get Device association")
    status, retdata = self.rest_get(url, expret=[200])

    if not status or retdata["result"] not in ["FETCH_PATIENT_INVENTORY_SUCCESS"]:
        return [False, []]

    return [True, retdata["response"]["patch_patient_map"]]


def detach_sensor(self, pid, devices, dryrun=False):
    print("Detach all sensors using rest api from patient %s ...." % pid)

    if self._tenant is None: self.start()

    currlist = [s["patches.patch_type"] for s in devices]
    for s in devices:
        currlist.remove(s["patches.patch_type"])
        sdata = {
            "patch_uuid": s["patch_uuid"],
            "type_device": s["patches.patch_type"],
            "associated_list": currlist,
            "action": "unassociate",
            "pid": pid,
            "patch_serial": s["patches.device_serial"]
        }
        if len(currlist) == 0:
            sdata["patch_serial"] = ""

        self.log_info("Detach Devices: %s" % json.dumps(sdata))
        url = "api/patients"
        if dryrun:
            continue

        status, retdata = self.rest_delete(url, data=sdata, expret = [200])
        if not status or retdata["Code"] not in ["UNASSOCIATE_SUCCESS"] :
            return False

    return True


if __name__ == "__main__":
    import libs.rest.restlibs as restlibs

