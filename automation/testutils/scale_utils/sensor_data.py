import time
import random

def  set_random_seed(seed):
    if seed is None:
        seed = time.time()

    print("Using Seed value: %d", seed)
    random.seed(seed)

def get_random_battery(battery):
    battery -= random.randint(0,5)
    if battery < 0:
        battery = 100

    return battery

def create_ecg_data(prevecg, randdiff = 200):
    if prevecg is None:
        return [
            -740, -745, -735, -747, -737, -733, -735, -719,
            -741, -714, -713, -704, -701, -700, -697, -693,
            -691, -700, -698, -707, -686, -682, -692, -678,
            -661, -633, -627, -630, -635, -655, -667, -649,
            -650, -653, -648, -659, -800, -1116, -959, 148,
            1458, 1619, 698, -362, -568, -668, -737, -768,
            -799, -791, -789, -799, -811, -832, -868, -1090,
            -1131, -1146, -1160, -1193, -1189, -1197, -1196, -1183,
            -1169, -1148, -1125, -1092, -1050, -1009, -1000, -976,
            -971, -969, -968, -971, -968, -974, -952, -953,
            -947, -955, -946, -950, -954, -950, -944, -944,
            -963, -944, -946, -944, -946, -936, -940, -934,
            -925, -931, -926, -943, -920, -924, -920, -922,
            -920, -920, -917, -914, -908, -904, -907, -861,
            -874, -884, -891, -909, -909, -910, -910, -912,
            -918, -952, -1196, -1364, -840, 486, 1374, 830
     ]
    diff = random.randint(1, randdiff)
    r1 = random.randint(30, 40)
    r1d = r1 + random.randint(2, 3)
    r1s = r1d + random.randint(3, 4)
    r1d2 = r1s + random.randint(3, 4)
    r2 = r1s + random.randint(6, 10)
    r3 = r2 + random.randint(6, 10)
    r4 = r3 + random.randint(30, 40)
    r4d = r4 + random.randint(2, 3)
    r4s = r4d + random.randint(3, 4)
    r5 = 128 - r4s
    if r5 < 0: r5 = 10

    c1 = [random.randint(-800, -650) for i in range(0, r1)]
    c2 = [random.randint(-1193, -970) for i in range(r1, r1d)]
    c3 = [random.randint(200, 1170) for i in range(r1d, r1s)]
    c4 = [random.randint(-630, -362) for i in range(r1s, r1d2)]
    c4.sort()
    if random.randint(1, 10) % 2:
        c5 = [random.randint(-800, -650) for i in range(r1d2, r2)]
        c6 = [random.randint(-800, -650) for i in range(r2, r3)]
    else:
        c5 = [random.randint(-740, -720) for i in range(r1d2, r2)]
        c6 = [random.randint(-760, -720) for i in range(r2, r3)]

    c7 = [random.randint(-1200, -1080) for i in range(r3, r4)]
    c8 = [random.randint(-1200, -1080) for i in range(r4, r4d)]
    c9 = [random.randint(200, 1170) for i in range(r4d, r4s)]
    c10 = [random.randint(-800, -650) for i in range(0, r5)]
    final = c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9 + c10
    return final[:128]

def simulate_ecg_data(restobj, patient_id, type, duration, mac, freq=0, seed=None, currecg=None):
    print("Sending ECG data")
    set_random_seed(seed=seed)

    data = {
        "battery": 100,
        "HR": 102,
        "RR": 20,
        "battery": 100,
        "ecg": [],
        "mac": mac
    }

    #currecg = None
    battery = 100
    starttime = time.time()
    idx = 0
    while time.time() - starttime < duration:
        if idx: time.sleep(freq)
        idx += 1
        if freq > 10 or idx % 10 == 0:
            data["battery"] = battery = get_random_battery(battery=battery)

        alert = random.randint(2, 20)
        if idx % alert == 0:
            lohi = random.randint(0, 1)
            data["HR"] = [random.randint(101, 120), random.randint(45, 59)][lohi]
            data["RR"] = [random.randint(26, 35), random.randint(15, 19)][lohi]
        else:
            data["HR"] = random.randint(90, 100)
            data["RR"] = random.randint(20, 25)

        data["ecg"] = create_ecg_data(prevecg=currecg)
        currecg = data["ecg"]

        if restobj is not None:
            restobj.send_sensor_data(patient_id, type, data, ts=time.time())

        if freq == 0:
            return currecg
def create_viatom_data(prevecg, randdiff = 200):
    if prevecg is None:
        return [
            -0.037008327,-0.02960666,-0.009868887,-0.046877213,-0.05921332,-0.022204995,-0.009868887,0.01480333,
             0.04440999,0.051811658,0.024672218,-0.007401665,-0.017270552,-0.034541104,-0.04440999,
            -0.034541104,-0.019737775,-0.0024672218,-0.012336109,-0.017270552,0.22204995,0.8388554,
            1.3224308,0.27386162,-0.9770198,-1.0090936,-0.3158044,-0.0912872,-0.03207388,-0.007401665,
            0.0049344436,0.034541104,0.061680544,0.0567461,0.0789511,0.08141832,0.103623316,0.10609053,
            0.120893866,0.14556608,0.1579022,0.18504164,0.20724663,0.23438606,0.26892716,0.29113215,
            0.33307493,0.34294382,0.36021438,0.3651488,0.31086993,0.30100104,0.25165662,0.18997607,
            0.120893866,0.0567461,0.027139438,-0.01480333,-0.061680544,-0.0789511,-0.093754426,-0.0789511,
            -0.093754426,-0.09622165,-0.06414776,-0.054278877,-0.04440999,-0.034541104,-0.019737775,-0.0049344436,
            -0.019737775,-0.007401665,-0.0024672218,-0.017270552,-0.009868887,-0.012336109,0,-0.017270552,-0.027139438,
            -0.017270552,-0.01480333,-0.03207388,-0.027139438,-0.022204995,-0.017270552,-0.024672218,-0.022204995,
            -0.03207388,-0.03947555,-0.041942768,0.0049344436,0.05921332,0.066614985,0.0567461,0.05921332,
            0.009868887,0,-0.022204995,-0.02960666,0,-0.0049344436,-0.012336109,-0.009868887,
            0.009868887,0.24672218,0.85612595,1.3495703,0.28126326,-0.9844215,-0.99429035,-0.28619772,
            -0.05921332,0.0049344436,0.022204995,0.019737775,0.04440999,0.05921332,0.049344435,0.0912872,
            0.083885536,0.10855775,0.10115609,0.13816442,0.16777107,0.16530386,0.19491051,0.2171155,0.25165662
     ]
    diff = random.randint(1, randdiff)
    r1 = random.randint(30, 40)
    print(r1)
    r1d = r1 + random.randint(2, 3)
    r1s = r1d + random.randint(3, 4)
    r1d2 = r1s + random.randint(3, 4)
    r2 = r1s + random.randint(6, 10)
    r3 = r2 + random.randint(6, 10)
    r4 = r3 + random.randint(30, 40)
    r4d = r4 + random.randint(2, 3)
    r4s = r4d + random.randint(3, 4)
    print("r4s {}".format(r4s))
    r5 = 128 - r4s
    #print("r55 {}".format(r5))
    if r5 < 0: r5 = 10

    c1 = [random.randint(-800, -650) for i in range(0, r1)]
    c2 = [random.randint(-1193, -970) for i in range(r1, r1d)]
    c3 = [random.randint(200, 1170) for i in range(r1d, r1s)]
    c4 = [random.randint(-630, -362) for i in range(r1s, r1d2)]
    c4.sort()
    if random.randint(1, 10) % 2:
        c5 = [random.randint(-800, -650) for i in range(r1d2, r2)]
        c6 = [random.randint(-800, -650) for i in range(r2, r3)]
    else:
        c5 = [random.randint(-740, -720) for i in range(r1d2, r2)]
        c6 = [random.randint(-760, -720) for i in range(r2, r3)]

    c7 = [random.randint(-1200, -1080) for i in range(r3, r4)]
    c8 = [random.randint(-1200, -1080) for i in range(r4, r4d)]
    c9 = [random.randint(200, 1170) for i in range(r4d, r4s)]
    c10 = [random.randint(-800, -650) for i in range(0, r5)]
    final = c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9 + c10
    return final[:128]

def simulate_viatom_data(restobj, patient_id, type, duration, mac, freq=0, seed=None, currecg=None):
    print("Sending ECG data")
    set_random_seed(seed=seed)

    data = {
        "battery": 100,
        "HR": 102,
        "RR": 20,
        "battery": 100,
        "ecg": [],
        "mac": mac
    }


    battery = 100
    starttime = time.time()
    idx = 0

    while time.time() - starttime < duration:

        if idx: time.sleep(freq)
        idx += 1
        if freq > 10 or idx % 10 == 0:
            data["battery"] = battery = get_random_battery(battery=battery)
        currecg = None
        alert = random.randint(2, 20)
        if idx % alert == 0:
            lohi = random.randint(0, 1)
            data["HR"] = [random.randint(101, 120), random.randint(45, 59)][lohi]
            data["RR"] = [random.randint(26, 35), random.randint(15, 19)][lohi]
        else:
            data["HR"] = random.randint(90, 100)
            data["RR"] = random.randint(20, 25)
        #print("currecg {}".format(currecg))
        data["ecg"] = create_viatom_data(prevecg=currecg)
        currecg = data["ecg"]

        if restobj is not None:
            restobj.send_sensor_data(patient_id, type, data, ts=time.time())

        if freq == 0:
            return currecg


def simulate_bp_data(restobj, patient_id, type, duration, mac, freq=0, seed=None):
    print("Sending BP data for type", type)
    set_random_seed(seed=seed)
    battery = 100
    data = {
        "bpd": 100,
        "bps": 60,
        "mac": mac
    }

    idx = 0
    starttime = time.time()
    while time.time() - starttime < duration:
        if idx: time.sleep(freq)
        idx +=1
        data["bps"] = random.randint(110, 120)
        data["bpd"] = random.randint(70,80)
        data["heartRate"] = random.randint(77,80)
        data["battery"] = get_random_battery(battery=battery)

        if idx % 20 == 0:
            data["bpd"] = random.randint(80, 98)
        elif idx % 10 == 0:
            data["bps"] = random.randint(121, 150)

        restobj.send_sensor_data(patient_id=patient_id, type=type, data=data, ts=time.time())
        if freq == 0:
            return


def simulate_spo2_data(restobj, patient_id, type, duration, mac, freq=0, seed=None):
    print("Sending SPO2 data")
    set_random_seed(seed=seed)
    data = {"spo2": 97, "battery": 70, "pi": 20, "pr": 20, "mac": mac}

    battery = 100
    starttime = time.time()
    idx = 0
    while time.time() - starttime < duration:
        if idx: time.sleep(freq)
        idx += 1
        data["battery"] = battery = get_random_battery(battery=battery)
        data["spo2"] = random.randint(90, 100)
        data["pi"] = random.randint(90, 100)
        data["pr"] = random.randint(90, 100)
        if idx % 10 == 0:
            data["spo2"] = random.randint(80, 89)
        restobj.send_sensor_data(patient_id=patient_id, type=type, data=data, ts=time.time())
        if freq == 0:
            return


def simulate_temp_data(restobj, patient_id, type, duration, mac, freq=0, seed=None):
    print("Sending Temperature data", type)
    set_random_seed(seed=seed)
    data = {"battery": 70, "value": 98.4, "mac": mac}

    battery = 100
    starttime = time.time()
    idx = 0
    while time.time() - starttime < duration:
        if idx: time.sleep(freq)
        idx += 1
        data["battery"] = battery = get_random_battery(battery=battery)
        data["value"] = round(random.uniform(94.1, 98.4), 2)
        if idx % 10 == 0:
            data["value"] = round(random.uniform(98.6, 104.5), 2)
        restobj.send_sensor_data(patient_id=patient_id, type=type, data=data, ts=time.time())
        if freq == 0:
            return


def simulate_digital_data(restobj, patient_id, type, duration, mac, freq=0, seed=None):
    print("Sending Digital data")
    set_random_seed(seed=seed)
    data = {"weight": 160, "mac": mac}

    starttime = time.time()
    idx = 0
    while time.time() - starttime < duration:
        if idx: time.sleep(freq)
        idx += 1
        data["weight"] = random.randint(160, 170)
        restobj.send_sensor_data(patient_id=patient_id, type=type, data=data, ts=time.time())
        if freq == 0:
            return


def simulate_keepalive_data(restobj, patient_id, type, duration, mac, freq=0, seed=None):
    print("Sending Keep Alive data")
    set_random_seed(seed=seed)
    data = {"battery": 90, "mac": mac}

    battery = 100
    starttime = time.time()
    idx = 0
    while time.time() - starttime < duration:
        if idx: time.sleep(freq)
        data["battery"] = battery = get_random_battery(battery=battery)
        idx += 1
        restobj.send_sensor_data(patient_id=patient_id, type=type, data=data, ts=time.time())
        if freq == 0:
            return


def simulate_data(restobj, mrn, patient, duration=120):
    stime = time.time()
    cnt = 0
    currecg = None
    ptype = patient["demographic_map"]["patient_type"]
    pid = patient["demographic_map"]["pid"]
    print("Patient UUID:", pid)
    status, devassoc = restobj.get_device_association(patient=pid)
    if len(devassoc) == 0:
        print("No Sensors associated")
        return
    while (time.time() - stime) < duration:
        for dev in devassoc:
            type = dev["patches.patch_type"]
            mac = dev["patches.patch_mac"]
            if type.lower() == 'spo2' and (cnt % 600) == 0:
                simulate_spo2_data(restobj=restobj, patient_id=pid, type=type, duration=duration, freq=0, mac=mac)
            if type.lower() == "ihealth" and (cnt % (2 * 3600)) == 0:
                simulate_bp_data(restobj=restobj, patient_id=pid, type=type, duration=duration, freq=0, mac=mac)
            if type.lower() == "alphamed" and (cnt % (2 * 3600)) == 0:
                simulate_bp_data(restobj=restobj, patient_id=pid, type=type, duration=duration, freq=0, mac=mac)
            if type.lower() == "ecg" and (cnt % 1) == 0:
                currecg = simulate_ecg_data(restobj=restobj, patient_id=pid, type=type, duration=duration, freq=0, mac=mac, currecg=currecg)
            if type.lower() == "viatom" and (cnt % 1) == 0:
                currecg = simulate_viatom_data(restobj=restobj, patient_id=pid, type=type, duration=duration, freq=0, mac=mac, currecg=currecg)
            if type.lower() == "temperature" and (cnt % (3 * 3600)) == 0:
                 simulate_temp_data(restobj=restobj, patient_id=pid, type=type, duration=duration, freq=0, mac=mac)
            if type.lower() == "digital" and (cnt % (6 * 3600)) == 0:
                simulate_digital_data(restobj=restobj, patient_id=pid, type=type, duration=duration, freq=0, mac=mac)
            if type.lower() == "gw" and (cnt % 60) == 0:
                simulate_keepalive_data(restobj=restobj, patient_id=pid, type=type, duration=duration, freq=0, mac=mac)
        time.sleep(1)
        cnt = cnt + 1
