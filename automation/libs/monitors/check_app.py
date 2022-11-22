import requests

import os
import json
import sys
import traceback

opt  = int(sys.argv[1])

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

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

token = "xoxb-3309400753206-3797230774931-VqxggShgtICPVUdJpsxOS5Oo"
slackdata = {
            'token': token,
            'channel': 'D03PHLZT3NG',
            'as_user': True,
            'text': ""
        }
slackdata["channel"] = "C03PF27JMKM"

for tb in ["/home/sriniadmin/vm3.yaml", "/home/sriniadmin/mnj.yaml"]:
    request = Request()
    request.config.option.tbfile = tb
    request.config.option.runparams = "{}"

    futils.start_test(request=request, startweb=False)
    tbobj = request.config.option.tbobj
    solobj = live247.Live247(tbobj=tbobj)

    solobj.set_ui("rest")
    weburl = tbobj.tbinfo["web"]["url"]
    resturl = tbobj.tbinfo["rest"]["url"]
    try:
        solobj._restlib.start()
        status,ret = solobj._restlib._get_patient_inventory(limit=1, offset=1)
        stage = "back-end"
        if ret["patientTotalCount"] <= 0:
            raise
        stage = "front-end"
        sess = requests.Session()
        res = sess.get(weburl, timeout=10)
        if res.status_code not in [200] or "Live247" not in res.text:
            print(res.text)
            raise

        if opt:
            msg = "%s is stable - web: %s, rest: %s" % (tbobj.tbinfo["name"], weburl, resturl)
            slackdata["text"] = msg
            res = requests.post(url='https://slack.com/api/chat.postMessage', data=slackdata)
            print(res.text)
    except:
        traceback.print_exc()
        msg = "Failed to get patient details from %s (%s) - web: %s, rest: %s" % (tbobj.tbinfo["name"], stage, weburl, resturl)

        slackdata["text"] = msg
        res = requests.post(url='https://slack.com/api/chat.postMessage', data=slackdata)
        print(res.text)

