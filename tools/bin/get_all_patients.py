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
import automation.testutils.scale_utils.sensor_data as scale_sensorlib

parser = argparse.ArgumentParser(description='Get all hospital')
parser.add_argument('-T', '--tenant', dest='tenant', help="Tenant name")
parser.add_argument('-S', '--saasurl', dest='saasurl', help="SaaS URL http://40.112.217.42:7141", default="http://40.112.217.42:7124")
parser.add_argument('-U', '--saasuser', dest='saasuser', help="SaaS User", default="demo@gmail.com")
parser.add_argument('-P', '--saaspassword', dest='saaspassword', help="SaaS User", default="admin123")

args = parser.parse_args()
print(args)
restobj = restlibs.RestLibs({"url": args.saasurl, "username": args.saasuser, "password": args.saaspassword})

# Get Tenant ID based on name. If this api results in None, then try to use old log
if args.tenant is None:
    restobj.login()
else:
    tenantid = restobj.get_tenant_id(name=args.tenant)
    restobj.login(tenantid=tenantid)

patientdata = restobj.get_patient_inventory(type="Hospital")

print(patientdata)
with open("patients.json", "w") as fd:
    json.dump(patientdata, fd,  indent=4)