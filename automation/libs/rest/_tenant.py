def get_all_tenants(self):
    url = "api/tenant"
    self.log_info("Get Tenants")
    status, retdata = self.rest_get(url, expret=[200, 440])

    if not status or retdata["Code"] not in ["FETCH_TENANTS_SUCCESS"]:
        return [False, []]

    return [True, retdata["response"]["data"]]


def get_tenant_id(self: object, name: object)  -> object:
    status, tenants = self.get_all_tenants()
    for t in tenants:
        if t["tenants.tenant_name"] == name:
            return t['tenants.tenant_uuid']

    return None


if __name__ == "__main__":
    import libs.rest.restlibs as restlibs
