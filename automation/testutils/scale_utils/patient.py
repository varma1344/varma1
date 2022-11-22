import datetime
import json
import os
import random

import testutils.scale_utils.consts as consts

def generate_patients(type, count, datafile, basename="AT", country="United States"):
    retval = []

    titles = [["Mr.", "Male"], ["Mrs.", "Female"], ["Ms.", "Female"]]
    CONST=consts.COUNTRY[country]

    for i in range(count):
        day = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 60))
        t = titles[random.randint(0,2)]
        phone = "%s%s%s%03d" % (CONST["phonecode"], CONST["%s_phone_pre" % type.lower()], "000", i)
        admission_date = "%s-%02d-%02d" % (day.year, day.month, day.day) if type.lower() == "hospital" else ""
        data = {
            "admission_date": admission_date,
            "title": t[0], "fname": "Pat%08d" % (basename, i), "mname": "M%d" % (i),
            "lname": "%s%03d" % (basename, random.randint(1, 999)),
            "med_record": "%sMRN%08d" % (basename, i),
            "sex": t[1],
            "DOB": "%s-%02d-%02d" % (random.randint(1977, 2005), random.randint(1, 12), random.randint(1, 28)),
            "phone_contact": phone, "country_name": CONST["name"], "patient_type": type
        }
        retval.append(data)

    str = "[\n"
    isfirst = True
    for d in retval:
        if not isfirst:
            str += ",\n"
        isfirst = False
        str += "%s" % json.dumps(d)
    str += "\n]"
    with open(datafile, "w") as fd:
        fd.write(str)

    return retval


if __name__ == "__main__":
    datafile = os.path.join("..", "..", "testdata", "scale_patients1k_2.json")
    generate_patients(count=1000, datafile=datafile, basename="ATEx2")



