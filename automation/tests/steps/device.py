import pytest
from pytest_bdd import when, then, given, parsers
import libs.utils as utils
import libs.live247 as live247

@pytest.fixture
@given(parsers.parse('Below sensor details stored in {datavar}:\n{data}'))
def store_sensor_data(request, datavar, data):
    input = request.config.option.input
    input[datavar] = utils.parse_str_table(data)
    print(input)

@when(parsers.parse("we add devices based on data stored in {datavar}"))
def add_sensors(request, datavar):
    sensors = request.config.option.input[datavar]
    solobj = request.config.option.solution
    for s in sensors:
        assert solobj.add_sensors(sensors=[s]), "Adding sensors failed"
