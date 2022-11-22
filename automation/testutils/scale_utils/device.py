import datetime
import json
import os
import random

import testutils.scale_utils.consts as consts

def generate_devices(startidx, endidx, datafile=None, basename="AT", bmac="10:01", sbmac="10:02"):
    retval = []

    sensors = consts.SENSORS
    for gi in range(startidx, endidx+1):
        mac = "%s:%02x:%02x:%02x" % (bmac, (gi >> 16) & 0xff, (gi >> 8) & 0xff, gi & 0xff)
        gwdata = {"patch_type": "gateway", "device_serial": "%sg%04d" % (basename, gi), "patch_mac": mac,
                  "sim": 80000000 + gi, "tags": ["gw%04d" % gi]}
        #retval.append(gwdata)

        sensorlist = []
        for i,s in enumerate(sensors):
            pt = s[random.randint(0,len(s) - 1)]
            mac = "%s:%02x:%02x:%02x" % (sbmac, (gi >> 8) & 0xff, gi & 0xff, i & 0xff)
            data = {"patch_type": pt, "device_serial": "%sg%04ds%d" % (basename, gi, i), "patch_mac": mac,
                    "tags": ["gw%04d" % gi]}
            sensorlist.append(data)

        retval.append([gwdata, sensorlist])

    if datafile is not None:
        final_str = "[\n"
        isfirstgw = True
        for devmap in retval:
            if not isfirstgw:
                final_str += ",\n"
            isfirstgw = False

            final_str += "[%s," % json.dumps(devmap[0])
            str = "[\n"
            isfirst = True
            for d in devmap[1]:
                if not isfirst:
                    str += ",\n"
                isfirst = False
                str += "%s" % json.dumps(d)
            str += "\n]"
            final_str = "%s\n%s]" % (final_str, str)
        final_str += "\n]"

        with open(datafile, "w") as fd:
            fd.write(final_str)

    return retval


if __name__ == "__main__":
    datafile = os.path.join("..", "..", "testdata", "scale_devices.json")
    generate_devices(count=500, datafile=datafile)



