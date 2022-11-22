"""
Create Users
For example:
   Tenant: Demo Hospital 01
   Create Doctors
   python3 create_users.py -S http://us.livehealthyvibes.com:7124 -U admin@ushospital.com -P admin123 -T "Demo Hospital 01" -B Demo01 --usertype Doc --startidx 2 --endidx 10
   python3 create_users.py -S http://us.livehealthyvibes.com:7124 -U admin@ushospital.com -P admin123 -T "Demo Hospital 01" -B Demo01 --usertype Nurse --startidx 3 --endidx 10
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
import automation.testutils.scale_utils.users as userlib

parser = argparse.ArgumentParser(description='Create Doc or Nurse users')
parser.add_argument('-T', '--tenant', dest='tenant', help="Tenant name")
parser.add_argument('-B', '--basename', dest='basename', help="Base Name used for mrn, email, etc")
parser.add_argument('-S', '--saasurl', dest='saasurl', help="SaaS URL http://40.112.217.42:7141")
parser.add_argument('-U', '--saasuser', dest='saasuser', help="SaaS User")
parser.add_argument('-P', '--saaspassword', dest='saaspassword', help="SaaS User")
parser.add_argument('--usertype', dest='usertype', help="User Type")
parser.add_argument('--startidx', dest='startidx', help="Start index used for names", default=0)
parser.add_argument('--endidx', dest='endidx', help="End index used for names", default=0)
parser.add_argument('--country', dest='country', help="Country Name", default="usa")

args = parser.parse_args()
print(args)

restobj = restlibs.RestLibs({"url": args.saasurl, "username": args.saasuser, "password": args.saaspassword})
userlist = userlib.generate_users(type=args.usertype[:3], basename=args.basename,
                                  startidx=int(args.startidx), endidx=int(args.endidx), country=args.country)
for u in userlist:
    print(u)

# Get Tenant ID based on name. If this api results in None, then try to use old log
tenantid = restobj.get_tenant_id(name=args.tenant)
if tenantid is None:
    print("Unable to find tenant")
    sys.exit(1)

restobj.login(tenantid=tenantid)
role_uuid = restobj.get_roles_id(name=args.usertype)
print(role_uuid)

for u in userlist:
    restobj.add_user(indata=u, tenant_id=tenantid, role_uuid=role_uuid)


