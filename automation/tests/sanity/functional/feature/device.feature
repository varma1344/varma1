Feature: Device Functional Tests
    Tests to validate device CURD operations.

    Scenario: Create and delete sensors
        When Test stated
        Given Below sensor details stored in "SENSORS":
            | serial       | type                 |  macaddress       |
            | arungw01s01    | ECG Sensor             | 00:11:22:33:01:01 |
        When we add devices based on data stored in "SENSORS"
        Then Test ended
