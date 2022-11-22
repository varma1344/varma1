class TestTopo:
    def __init__(self, tbinfo, runparms):
        self.tbinfo = tbinfo
        self.runparams = runparms

    def get_web_info(self):
        return self.tbinfo["web"]

    def get_rest_info(self):
        return self.tbinfo["rest"]
