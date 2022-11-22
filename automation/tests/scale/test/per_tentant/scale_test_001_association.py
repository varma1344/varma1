import os
import json
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

import testutils.framework_utils as futils
import libs.live247 as live247

class Option:
    def __init__(self):
        self.tbfile = None
        self.runparams = None
        self.solution = None
        self.input = None
        self.tbobj = None

class Config:
    def __init__(self):
        self.option = Option()

class Request:
    def __init__(self):
        self.config = Config()

request = Request()
request.config.option.tbfile = "C:/Users/arunmandava/live247/Automation/testbeds/scale/testbed1.yaml"
request.config.option.runparams = "{}"

futils.start_test(request=request, startweb=False)

def create_assoc(plist, dlist, allplist, alldlist):
    try:
        solobj = live247.Live247(tbobj=request.config.option.tbobj)
        solobj.set_ui("rest")

        if not solobj.associate_sensors(patients=plist, devlist=dlist, alldlist=alldlist, allplist=allplist):
            pass
    except:
        print("Failed in associate device")

datafile = os.path.join(os.path.join(os.path.dirname(__file__)), "..", "..", "..", "..", "testdata", "scale_devices.json")
with open(datafile, "r") as fd:
    devices = json.load(fd)

datafile = os.path.join(os.path.join(os.path.dirname(__file__)), "..", "..", "..", "..", "testdata", "scale_patients.json")
with open(datafile, "r") as fd:
    patients = json.load(fd)

import threading

solobj = live247.Live247(tbobj=request.config.option.tbobj)
allpatients = solobj.get_all_patients()
alldevs = solobj.get_all_devices()
tobjs = {}
tcnt = 25
patients = patients[76:]
devices = devices[76:]
for i in range(0, 1):
    tobjs[i] = threading.Thread(target=create_assoc, args=(patients[i * tcnt: (i * tcnt) + tcnt],
                                                             devices[i * tcnt: (i * tcnt) + tcnt],
                                                             allpatients, alldevs))

for i in tobjs:
    tobjs[i].start()
    tobjs[i].join()


# fstr = ""
# for i in tobjs:
#     tobjs[i].join()
#     #fstr += "Thread %s finished\n" % i
# print("Threads completed\n", fstr)

futils.end_test(request=request)

