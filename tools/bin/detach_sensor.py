"""
Associate Sensors to patients
   python3 detach_sensor.py -S http://us.livehealthyvibes.com:7124 -U demoadmin01@live247.com -P admin123 -T "Demo Hospital 01" --startidx 1 --endidx 10
"""
import argparse
import json
import os
import random
import time
import sys
import traceback

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "automation"))
print(os.path.join(os.path.dirname(__file__), "..", "..", "automation"))

import automation.libs.rest.restlibs as restlibs
import automation.testutils.scale_utils.device as devrlib

parser = argparse.ArgumentParser(description='Create Doc or Nurse users')
parser.add_argument('-T', '--tenant', dest='tenant', help="Tenant name")
parser.add_argument('-B', '--basename', dest='basename', help="Base Name used for mrn, email, etc")
parser.add_argument('-S', '--saasurl', dest='saasurl', help="SaaS URL http://40.112.217.42:7141")
parser.add_argument('-U', '--saasuser', dest='saasuser', help="SaaS User")
parser.add_argument('-P', '--saaspassword', dest='saaspassword', help="SaaS User")
parser.add_argument('-D', '--duration', dest='duration', help="Duration in secs", default=120)
parser.add_argument('--basemac', dest='basemac', help="Base mac address to use. e.g., 10:00")
parser.add_argument('-M', '--mrn', dest='mrn', help="Patient MRN")
parser.add_argument('--startidx', dest='startidx', help="Start index used for names", default=0)
parser.add_argument('--endidx', dest='endidx', help="End index used for names", default=0)
parser.add_argument('--backdays', dest='backdays', help="Associate sensor start date", default=0)
parser.add_argument('--ptype', dest='ptype', help="Patient Type", default="Hospital")

args = parser.parse_args()
print(args)

startidx=int(args.startidx)
endidx=int(args.endidx)
duration = int(args.duration)

restobj = restlibs.RestLibs({"url": args.saasurl, "username": args.saasuser, "password": args.saaspassword})

# Get Tenant ID based on name. If this api results in None, then try to use old log
tenantid = restobj.get_tenant_id(name=args.tenant)
if tenantid is None:
    print("Unable to find tenant")
    sys.exit(1)

restobj.login(tenantid=tenantid)

if args.mrn:
    mrn = args.mrn
    cnt, patientdata = restobj.get_patient_by_mrn(mrn=mrn, loc=args.ptype)
    status, devassoc = restobj.get_device_association(patient=patientdata["pid"])
    restobj.detach_sensor(pid=patientdata["pid"], devices=devassoc, dryrun=False)
else:
    patientdata = restobj.get_patient_inventory(type=args.ptype)
    mrnlist = list(patientdata.keys())
    mrnlist.sort()
    for mrn in mrnlist[startidx-1:endidx]:
        status, devassoc = restobj.get_device_association(patient=patientdata[mrn]["demographic_map"]["pid"])
        restobj.detach_sensor(pid=patientdata[mrn]["demographic_map"]["pid"], devices=devassoc, dryrun=True)

