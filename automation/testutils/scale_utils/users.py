import random

import testutils.scale_utils.consts as consts

def generate_users(type, basename, startidx, endidx, country="usa"):
    """Generate Users """
    userlist = []
    CONST=consts.COUNTRY[country]
    title = ["Mr.", "Mrs.", "Ms."]
    for idx in range(startidx, endidx+1):
        fname = "%s%02d" % (type.title(), idx)
        phone = "%s%s%s%03d" % (CONST["phonecode"], CONST["%s_phone_pre" % type.lower()], "000", idx)
        email = "%s%s%02d@live247.com" % (basename.lower(), type.lower(), idx)
        user = {
            "title": title[random.randint(0, len(title) - 1)], "fname": fname, "lname": basename,
            "username": "%s%s" % (basename.lower(), fname.lower()),
            "password": "admin123", "phone": phone, "email": email
        }
        userlist.append(user)

    return userlist
