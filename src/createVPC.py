import connDbnApi as cda
import naverCloud as ncset

class Create():
    def __init__(self, api, origin, destination):
        self.origin = origin
        self.destination = destination
        # self.cc = cda.Connect(api=api, destination=destination)
        # self.conn = self.cc.connect_cockroachdb()
        # self.conn.autocommit = True
        # self.cur = self.conn.cursor()
        # self.nc = ncset.url_info()
        # self.code_candidate = ncset.code_candidate()
        # self.out_candidate = ncset.out_candidate()
        # self.col_name_mapper = ncset.col_name_mapper()
        # self.special_info = ncset.special_info()

    def run(self):
        ...