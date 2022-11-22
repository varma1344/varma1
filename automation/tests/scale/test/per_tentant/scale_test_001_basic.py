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

def create_patients(plist):
    try:
        solobj = live247.Live247(tbobj=request.config.option.tbobj)
        return solobj.create_patients(patients=plist)
    except:
        print("Failed in creating patient")

datafile = os.path.join(os.path.join(os.path.dirname(__file__)), "..", "..", "..", "..", "testdata", "scale_patients.json")
with open(datafile, "r") as fd:
    patients = json.load(fd)

import threading

tobjs = {}
for i in range(0, 50):
    tobjs[i] = threading.Thread(target=create_patients, args=(patients[i * 100: (i * 100) + 100],))

for i in tobjs:
    tobjs[i].start()
    #tobjs[i].join()


fstr = ""
for i in tobjs:
    tobjs[i].join()
    fstr += "Thread %s finished\n" % i
    print("Threads completed\n", fstr)

futils.end_test(request=request)
