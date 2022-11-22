import json
import math

class Device:
    DEVICE = "api/patch"
    INVENTORY = "api/patch/patchinventory"

def _get_device_inventory(self, offset=1, limit=100, search=None):
    """Get Device inventory"""
    data = {"tenantId": self._tenant,
            "offset": offset, "limit": limit,
            "search": ""}
    if search: data["search"] = search
    status,retval = self.rest_post(url=Device.INVENTORY, data=data)
    if not status or retval["Code"] not in ["FETCH_PATCH_INVENTORY_SUCCESS"]:
        return False,{}

    return status, retval["response"]


def get_device_inventory(self, search=None):
    """
    Get device inventory data.
    :return: [<True or False>, Data in dict format]
    """
    if self._tenant is None: self.start()

    retdata = {}
    maxofset = 1
    offset = 1
    limit = 1000
    while offset <= maxofset:
        status,retval = self._get_device_inventory(offset=offset, limit=limit, search=search)
        if offset == 1:
            pcnt = retval["patchTotalCount"]
            maxofset = math.ceil(pcnt/limit)

        if not status:
            print("Failed to get devices")
            return retdata

        for dev in retval["patches"]:
            retdata[dev["device_serial"]] = dev

        offset += 1

    return retdata


def add_device(self, indata, dryrun=False):
    """
    Add device to inventory
    :param indata: Input data in dict format with below keys (same are API):
            patch_type, patch_serial, and patch_mac
    :return:
    """
    if self._tenant is None: self.start()

    data = {
        "data": [
            {
                "patch_type": indata["patch_type"], "patch_status": "Active",
                "device_serial": indata["device_serial"],
                "tenant_id": self._tenant,
                "patch_mac": indata["patch_mac"], "tags": indata["tags"]
            }
        ],
        "tenantId": self._tenant,
        "actionType": "device"
        }
    if indata["patch_type"] in ["gateway"]:
        data["data"][0]["sim"] = indata["sim"]

    self.log_info("Add Device: %s" % json.dumps(data))
    if not dryrun:
        status, retdata = self.rest_post(Device.DEVICE, data=data, expret = [200, 470])
        if not status: return False
        return True if retdata["Code"] in ["CREATE_PATCH_SUCCESS", "SERIAL_NUMBER_IS_ALREADY_EXIST",
                                             "MAC_ADDRESS_IS_ALREADY_EXIST"] else False

    return True


def get_device_info(self, search):
    if self._tenant is None: self.start()

    data = {
        "limit": 1, "offset": 1,
        "tenantId": self._tenant,
        "search": search
    }
    self.log_info("Get Device: %s" % json.dumps(data))
    status, retdata = self.rest_post(Device.INVENTORY, data=data, expret = [200])
    if not status: return False
    return True if retdata["response"] in ["FETCH_PATCH_INVENTORY_SUCCESS"] else False


if __name__ == "__main__":
    import libs.rest.restlibs as restlibs

