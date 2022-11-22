import argparse
import os
import random
import time
import sys
import traceback

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "automation"))
print(os.path.join(os.path.dirname(__file__), "..", "..", "..", "automation"))

import automation.libs.rest.restlibs as restlibs
import automation.testutils.scale_utils.sensor_data as scale_sensorlib

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-T', '--type', dest='type', help="Sensor type. Valid values ecg, viatom, spo2, temp, bp_ihealth, bp_alphamed, digital, gw", default="spo2")
parser.add_argument('-H', '--tenant', dest="tenant", help="Test Tenant06",default="Test Tenant06")
parser.add_argument('-M', '--mrn', dest='mrn', help="SMRN0002", default="SMRN0002")
parser.add_argument('-L', '--patientloc', dest='patientloc', help="Patient Location, hospital or remote", default='hospital')
parser.add_argument('-D', '--duration', dest='duration', help="Duration in secs", default=120)
parser.add_argument('-F', '--freq', dest='freq', help="Freq in secs", default=1)
parser.add_argument('-S', '--saasurl', dest='saasurl', help="SaaS URL http://us.livehealthyvibes.com:7124", default="http://us.livehealthyvibes.com:7124")
parser.add_argument('-U', '--saasuser', dest='saasuser', help="SaaS URL", default="testtenant06@live247.com")
parser.add_argument('-P', '--saaspassword', dest='saaspassword', help="SaaS User", default="admin123")

args = parser.parse_args()
print(args)
duration = int(args.duration)
freq = int(args.freq)
restobj = restlibs.RestLibs({"url": args.saasurl, "username": args.saasuser, "password": args.saaspassword})

# Get Tenant ID based on name. If this api results in None, then try to use old log
if args.tenant is None:
    restobj.login()
else:
    tenantid = restobj.get_tenant_id(name=args.tenant)
    restobj.login(tenantid=tenantid)

cnt,patientdata = restobj.get_patient_by_mrn(mrn=args.mrn, loc=args.patientloc)
print("Patient UUID:", patientdata["pid"])
status,devassoc = restobj.get_device_association(patient= patientdata["pid"])

devmap = {}
for dev in devassoc:
    devmap[dev["patches.patch_type"]] = dev["patches.patch_mac"]

if args.type.lower() == 'spo2':
    scale_sensorlib.simulate_spo2_data(restobj=restobj, patient_id=patientdata["pid"], type=args.type,
                                       duration=int(args.duration), freq=int(args.freq), mac=devmap['spo2'])
elif args.type.lower() == "bp_ihealth":
    scale_sensorlib.simulate_bp_data(restobj=restobj, patient_id=patientdata["pid"], type='ihealth',
                                       duration=int(args.duration), freq=int(args.freq), mac=devmap['ihealth'])
elif args.type.lower() == "bp_alphamed":
    scale_sensorlib.simulate_bp_data(restobj=restobj, patient_id=patientdata["pid"], type='alphamed',
                                       duration=int(args.duration), freq=int(args.freq), mac=devmap['alphamed'])
elif args.type.lower() == "ecg":
    print("ecg")
    scale_sensorlib.simulate_ecg_data(restobj=restobj, patient_id=patientdata["pid"], type=args.type,
                                       duration=int(args.duration), freq=int(args.freq), mac=devmap['ecg'])
elif args.type.lower() == "viatom":
    print("viatom")
    scale_sensorlib.simulate_viatom_data(restobj=restobj, patient_id=patientdata["pid"], type=args.type,
                                      duration=int(args.duration), freq=int(args.freq), mac=devmap['ecg'])
elif args.type.lower() == "temp":
    print("temp")
    scale_sensorlib.simulate_temp_data(restobj=restobj, patient_id=patientdata["pid"], type="temperature",
                                       duration=int(args.duration), freq=int(args.freq), mac=devmap['temperature'])
elif args.type.lower() == "digital":
    scale_sensorlib.simulate_digital_data(restobj=restobj, patient_id=patientdata["pid"], type="digital",
                                       duration=int(args.duration), freq=int(args.freq), mac=devmap['digital'])
elif args.type.lower() == "gw":
    scale_sensorlib.simulate_keepalive_data(restobj=restobj, patient_id=patientdata["pid"], type="gw",
                                       duration=int(args.duration), freq=int(args.freq), mac=devmap['gateway'])


