import os

from pytest_bdd import scenario, scenarios

feat = os.path.join("..", "..", "functional", "feature", "device.feature")
scenarios(feat)

@scenario(feat, 'Create and delete sensors')
def test_add_delete_sesnors():
    pass
