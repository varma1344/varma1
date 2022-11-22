import json
import os
import traceback
import yaml

import testutils.testtopo as testtopo
import libs.live247 as live247

def start_test(request, startweb=True):
    print("Starting test: Testbed file: ", request.config.option.tbfile,
          "Runparams: ", request.config.option.runparams)

    if not request.config.option.tbfile:
        assert 0, "Testbed file option is (--tbfile) is mandatory."

    if not request.config.option.runparams:
        assert 0, "Runtime parameters option is (--runparams) is mandatory."

    if not os.path.isfile(request.config.option.tbfile):
        assert 0, "Testbed %s file is not found" % request.config.option.tbfile

    with open(request.config.option.tbfile) as fd:
        tbinfo = yaml.load(fd, yaml.Loader)

    # Run parameters can be given as JSON string or as file
    if os.path.isfile(request.config.option.runparams):
        with open(request.config.option.runparams) as fd:
            rpdata = json.load(fd)
    else:
        try:
            rpdata = json.loads(request.config.option.runparams)
        except:
            print(traceback.format_exc())
            return False

    request.config.option.tbobj = testtopo.TestTopo(tbinfo=tbinfo, runparms=rpdata)
    request.config.option.solution = live247.Live247(tbobj=request.config.option.tbobj)
    request.config.option.input = {}
    request.config.option.solution.login(start_web=startweb)
    return True

def end_test(request):
    request.config.option.solution.logout()
    print("Ending test")
    return True
