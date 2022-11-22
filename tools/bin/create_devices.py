"""
Create Devices
   python3 create_devices.py -S http://us.livehealthyvibes.com:7124 -U demoadmin01@live247.com -P admin123 -T "Demo Hospital 01" -B Demo01 --basemac 80:01 --startidx 1 --endidx 10
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
parser.add_argument('--basemac', dest='basemac', help="Base mac address to use. e.g., 10:00")
parser.add_argument('--startidx', dest='startidx', help="Start index used for names", default=0)
parser.add_argument('--endidx', dest='endidx', help="End index used for names", default=0)

args = parser.parse_args()
print(args)

restobj = restlibs.RestLibs({"url": args.saasurl, "username": args.saasuser, "password": args.saaspassword})
devlist = devrlib.generate_devices(startidx=int(args.startidx), endidx=int(args.endidx), basename=args.basename,
                                   bmac="%s:00" % args.basemac, sbmac="%s:01" % args.basemac)

# Get Tenant ID based on name. If this api results in None, then try to use old log
tenantid = restobj.get_tenant_id(name=args.tenant)
if tenantid is None:
    print("Unable to find tenant")
    sys.exit(1)

restobj.login(tenantid=tenantid)

for devs in devlist:
    restobj.add_device(indata=devs[0], dryrun=False)
    for d in devs[1]:
        restobj.add_device(indata=d, dryrun=False)


