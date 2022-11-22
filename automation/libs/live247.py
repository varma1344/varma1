"""
This module provides all the libraries at solution level.
"""
import time
import libs.web.weblibs as weblibs
import libs.rest.restlibs as restlibs
import os

class Live247:
    def __init__(self, tbobj):
        self.tbobj = tbobj
        self.senors = {}
        self.defaultui = "web"
        self.currui = "web"

        self._webinfo = tbobj.get_web_info()
        self._restinfo = tbobj.get_rest_info()
        self._weblib = weblibs.WebLibs(self._webinfo)
        self._restlib = restlibs.RestLibs(self._restinfo)

    def logout(self):
        self._weblib.stop_web()
        return True

    def login(self, start_web=False):
        if start_web:
            self._weblib.start_web()
            return self._weblib.login()

    def set_ui(self, ui):
        self.currui = ui

    def set_to_default_ui(self, ui):
        self.currui = self.defaultui

    def add_sensors(self, sensors):
        """
        Add given Sensors to the inventory
        :param sensors: List of sensor detail in dict format
        :return: Status True or False
        """
        ui = self.currui
        status = True
        for dev in sensors:
            print("Add Sensor", dev)
            if ui == "web":
                status &= self._weblib.add_device(serial=dev["serial"], type=dev["type"], details=dev)
            elif ui == "rest":
                status = self._restlib.add_device(dev)
                if not status:
                    print("   status: ", status)
                    return status

            print("   status: ", status)

        return status

    def del_sensors(self, sensors):
        """
        Delete Sensors from inventory
        :param sensors: List of sensor detail in dict format
        :return: Status True or False
        """
        """Delete Sensors from inventory"""
        ui = self.currui
        status = True
        for dev in sensors:
            if ui == "web":
                status &= self._weblib.delete_device(serial=dev["serial"], type=dev["type"])

        return status

    def create_patients(self, patients):
        for i,p in enumerate(patients):
            if not self._restlib.add_patient(indata=p):
                print("Creating Patient failed:", p)
                return False
        return True

    def get_all_patients(self):
        return self._restlib.get_patient_inventory()

    def get_all_devices(self):
        return self._restlib.get_device_inventory()
    
    def associate_sensors(self, patients, devlist, alldlist=None, allplist=None):
        idx = 0
        for p in patients:
            status = self._restlib.associate_sensors(patient=p, sensors=devlist[idx][1], 
                             gateway=devlist[idx][0], alldlist=alldlist, allplist=allplist)
            # if not status: 
            #     return status
            idx += 1
