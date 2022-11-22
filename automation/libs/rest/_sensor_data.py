import json
import traceback

def _form_alpamed_data(self, patient_id, data, ts):
    return  {
        "patientUUID": patient_id,
        "deviceType": "UrionBP",
        "bpd": data["bpd"],
        "bps": data["bps"],
        "timestamp":  ts
    }


def _form_ihealth_data(self, patient_id, data, ts):
    # return {
    #     "data":{
    #         "deviceID":"00:4D:32:0E:D7:D2", "deviceModel":"BP5S", "deviceName":"BP5S_004D320ED7D2",
    #         "extras":{
    #             "flash": False, "dataID":"79C8904E1CDA7FE0EBAF3EE2470039BB", "sys":127,
    #             "dia":81,"rssi":-55,"battery":-1,"heartRate":78,"hsdValue":False,
    #             "arrhythmia":False, "time":ts, "receiveTime":ts,
    #             "deviceInfo":{"function_measure_offline_open":1,
    #                           "options": {
    #                               "autoConnect":0,"connectRetry":5,"connectTimeout":10000,"extras":{},
    #                               "rssiThreshold":-95,"serviceDiscoverRetry":3,"serviceDiscoverTimeout":30000},
    #                           "function_max_memory_capacity":200,"upAirMeasureFlg":1,"model":"BP5S",
    #                           "fwVersion":"1.0.0","function_show_unit":0,"hwVersion":"1.0.0"}},
    #         "id":0, "time":1666516747000
    #     },
    #     "action":"ONLINE_RESULT_BP",
    #     "deviceType":"BP", "patientUUID":"patient364b691a-2bd7-42c0-984c-cda813f42ba4",
    #     "battery":100,"timestamp": ts
    # }
    return  {
        "patientUUID": patient_id,
        "deviceType": "BP",
        "battery": data["battery"],
        "data": {
            "deviceID": data["mac" ],
            "extras": {
                "sys": data["bps"],
                "dia": data["bpd"],
                "heartRate": data["heartRate"]
            }
        },
        "timestamp":  ts
    }

def _form_temperature_data(self, patient_id, data, ts):
    return  {
        "patientUUID": patient_id,
        "deviceType": "Temperature",
        "battery": data["battery"],
        "value": data["value"],
        "mac": data["mac" ],
        "deviceId": data["mac"],
        "timestamp":  ts
    }

def _form_spo2_data(self, patient_id, data, ts):
    return  {
        "patientUUID": patient_id,
        "deviceType": "checkme_O2",
        "spo2": data["spo2"],
        "battery": data["battery"],
        "pi": data["pi"],
        "pr": data["pr"],
        "timestamp":  ts
    }


def _form_ecg_data(self, patient_id, data, ts):
    return  {
        "patientUUID": patient_id,
        "gwBattery": data["battery"],
        "data": {
            "deviceID": data["mac"],
            "extras": {
                "HR": data["HR"],
                "RR": data["RR"],
                "battery": data["battery"],
                "ecg": data["ecg"]
            }
        },
        "deviceType": "vv330",
        "timestamp":  ts
    }
def _form_viatom_data(self, patient_id, data, ts):
    return  {
        "patientUUID": patient_id,
        "gwBattery": data["battery"],
        "data": {
            "deviceID": data["mac"],
            "extras": {
                "HR": data["HR"],
                "RR": data["RR"],
                "battery": data["battery"],
                "ecg": data["ecg"]
            }
        },
        "deviceType": "viatom",
        "timestamp":  ts
    }

def _form_digital_data(self, patient_id, data, ts):
    return  {
        "patientUUID": patient_id,
        "deviceType": "BodyFatScale",
        "weight": data["weight"],
        "timestamp":  ts
    }


def _form_keepalive_data(self, patient_id, data, ts):
    return {
        "version": "1.2102",
        "gwBattery": float(data["battery"]),
        "patientUUID": patient_id,
        "keep_alive_time": ts, "discovered_viva": ts - 100, "discovered_ble": ts - 100,
        "scan": False, "reset": False
    }


def send_sensor_data(self, patient_id, type, data, ts):
    if self._tenant is None: self.start()
    ts = int(ts) * 1000

    if type in ["alphamed"]:
        data = self._form_alpamed_data(patient_id=patient_id, data=data, ts=ts)
    elif type in ["ihealth"]:
        data = self._form_ihealth_data(patient_id=patient_id, data=data, ts=ts)
    elif type in ["temperature"]:
        data = self._form_temperature_data(patient_id=patient_id, data=data, ts=ts)
    elif type in ["spo2"]:
        data = self._form_spo2_data(patient_id=patient_id, data=data, ts=ts)
    elif type in ["viatom"]:
        data = self._form_viatom_data(patient_id=patient_id, data=data, ts=ts)
    elif type in ["ecg"]:
        data = self._form_ecg_data(patient_id=patient_id, data=data, ts=ts)
    elif type in ["digital"]:
        data = self._form_digital_data(patient_id=patient_id, data=data, ts=ts)
    elif type in ["gw"]:
        data = self._form_keepalive_data(patient_id=patient_id, data=data, ts=ts)

    self.log_info("Send Sensor data: %s" % json.dumps(data))
    url = "liveapi/gateway/gateway_keepalive" if type in ["keepalive"] else "liveapi/gateway/push_data"
    print(data)
    #return True
    try:	
        status, retdata = self.rest_post(url, data=data, expret = [200, 470])
    except:
        traceback.print_exc()
        print("Got exception when sending data")
        self._tenant = None
        self.start()
        status, retdata = self.rest_post(url, data=data, expret = [200, 470])
        
    if not status:
        return False

    return True
    #if retdata["result"] in ["CREATE_PATCH_SUCCESS"] else False

if __name__ == "__main__":
    import libs.rest.restlibs as restlibs

