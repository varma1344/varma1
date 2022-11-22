import os
import sys
import pytest

print(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import testutils.framework_utils as futils

def pytest_addoption(parser):
    parser.addoption("--tbfile", "-T", action="store", help="Testbed File name")
    parser.addoption("--runparams", "-R", action="store", help="Runtime file name or JSON")

from pytest_bdd import given, when, then

@when("Test stated")
def start_test_step(request):
    assert futils.start_test(request=request), "Start test failed"
    return

@then('Test ended')
def end_test_step(request):
    assert futils.end_test(request=request), "End test failed"
    return

pytest_plugins = [
   "tests.steps.device"
]
