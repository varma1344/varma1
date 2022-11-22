"""
python3 create_patients_fromfile.py -S http://us.livehealthyvibes.com:7124 -U demoadmin01@live247.com -P admin123 -T "Demo Hospital 01" -B Demo01 -M 1 -C live247download -F ./patients.json

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
import automation.testutils.scale_utils.sensor_data as scale_sensorlib

parser = argparse.ArgumentParser(description='Create patients based on JSON file')
parser.add_argument('-T', '--tenant', dest='tenant', help="Tenant name")
parser.add_argument('-S', '--saasurl', dest='saasurl', help="SaaS URL http://40.112.217.42:7141")
parser.add_argument('-U', '--saasuser', dest='saasuser', help="SaaS User")
parser.add_argument('-P', '--saaspassword', dest='saaspassword', help="SaaS User", default="admin123")
parser.add_argument('-F', '--patientsjson', dest='patientsjson', help="Patient data")
parser.add_argument('-B', '--basename', dest='basename', help="Base Name used for mrn, email, etc")
parser.add_argument('-C', '--dataformat', dest='dataformat', default="live247download",
                    help="Use patient data based on their type raw, live247download")
parser.add_argument('-M', '--mrnstart', dest='mrnstart', help="MRN start value", default=0)

args = parser.parse_args()
mrnstart = int(args.mrnstart)
mrnbase = "MRN%s" % args.basename

print(args)
restobj = restlibs.RestLibs({"url": args.saasurl, "username": args.saasuser, "password": args.saaspassword})

# Get Tenant ID based on name. If this api results in None, then try to use old log
tenantid = restobj.get_tenant_id(name=args.tenant)
restobj.login(tenantid=tenantid)

with open(args.patientsjson, "r") as fd:
    data = json.load(fd)

# Dict must have below elements
#temp = {"admission_date": "", "title": "", "fname": "", "mname": "", "lname": "", "med_record": "", "sex": "",
#        "DOB": "", "phone_contact": "",
#        "patient_type": "hospital", "country_name": "", "email": ""
#}

mrnlist = list(data.keys())
mrnlist.sort()
for i,k in enumerate(data):
    data[k]["demographic_map"]["med_record"] = "MRN%s%08d" % (args.basename, mrnstart + i)
    data[k]["demographic_map"]["tenant_id"] = tenantid

    if data[k]["demographic_map"]["country_name"] is None:
        data[k]["demographic_map"]["country_name"] = "United States"

    #if data[k]["demographic_map"]["email"] is None:
    data[k]["demographic_map"]["email"] = "%s@live247.com" % (data[k]["demographic_map"]["med_record"].lower())

    restobj.add_patient(data[k]["demographic_map"])
