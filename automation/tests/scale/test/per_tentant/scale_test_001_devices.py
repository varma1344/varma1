# import os
# import json
# import sys
#
# sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
#
# import testutils.framework_utils as futils
#
# class Option:
#     def __init__(self):
#         self.tbfile = None
#         self.runparams = None
#         self.solution = None
#         self.input = None
#         self.tbobj = None
#
# class Config:
#     def __init__(self):
#         self.option = Option()
#
# class Request:
#     def __init__(self):
#         self.config = Config()
#
# request = Request()
# request.config.option.tbfile = "C:/Users/arunmandava/live247/Automation/testbeds/scale/testbed1.yaml"
# request.config.option.runparams = "{}"
#
# futils.start_test(request=request, startweb=False)
#
# futils.end_test(request=request)
#
# solobj = request.config.option.solution
# datafile = os.path.join(os.path.join(os.path.dirname(__file__)), "..", "..", "..", "..", "testdata", "scale_devices.json")
# with open(datafile, "r") as fd:
#     devices = json.load(fd)
#
# solobj.set_ui("rest")
# for devmap in devices[55:]:
#     solobj.add_sensors(sensors = [devmap[0]])
#     solobj.add_sensors(sensors = devmap[1])
#


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

def create_devices(plist):
    try:
        solobj = live247.Live247(tbobj=request.config.option.tbobj)
        solobj.set_ui("rest")
        for devmap in plist:
             if not solobj.add_sensors(sensors = [devmap[0]]):
                 raise
             if not solobj.add_sensors(sensors = devmap[1]):
                 raise
    except:
        print("Failed in creating device")

datafile = os.path.join(os.path.join(os.path.dirname(__file__)), "..", "..", "..", "..", "testdata", "scale_devices.json")
with open(datafile, "r") as fd:
    devices = json.load(fd)

import threading

tobjs = {}
for i in range(0, 25):
    tobjs[i] = threading.Thread(target=create_devices, args=(devices[i * 20: (i * 20) + 20],))

for i in tobjs:
    tobjs[i].start()
    #tobjs[i].join()


fstr = ""
for i in tobjs:
    tobjs[i].join()
    #fstr += "Thread %s finished\n" % i
print("Threads completed\n", fstr)

futils.end_test(request=request)

