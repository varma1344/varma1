import os
import json
import pytest
import sys

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
print("XXXXXXXXXXXXXXXX", os.path.join(os.path.dirname(__file__)))

import testutils.framework_utils as futils

def pytest_addoption(parser):
    parser.addoption("--tbfile", "-T", action="store", help="Testbed File name")
    parser.addoption("--runparams", "-R", action="store", help="Runtime file name or JSON")

from pytest_bdd import given, when, then

class Test001:
    req = None
    _setup_done = False

    @pytest.fixture(autouse=True)
    def setup_method(self, request):
        print( request.config.option.tbfile)
        futils.start_test(request=request, startweb=False)
        self.req = request
        self._setup_done = True

    def teardown_method(self, method):
        futils.end_test(request=self.req)
        print(self.req.config.option.tbfile)
        print("stopping execution of tc: {}".format(method.__name__))

    def test_scale_001(self, request):
        solobj = request.config.option.solution
        datafile = os.path.join(os.path.join(os.path.dirname(__file__)), "..", "..", "..", "..", "testdata", "scale_patients.json")
        with open(datafile, "r") as fd:
            patients = json.load(fd)

        assert solobj.create_patients(patients=patients[:10]), "Creating Patients Failed"

