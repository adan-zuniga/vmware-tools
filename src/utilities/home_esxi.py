class ESXi:
    def __init__(self):
        self.host = '172.18.9.5'
        # self.host = '10.89.243.60'
        self.user = 'root'
        # self.user = 'uc-admin@acesandbox.local'
        self.password = 'l4bp$$D'
        # self.password = '8ic9D5V#67zE'
        self.port = 443
        self.disable_ssl_verification = True
        self.datacenter_name = 'ha-datacenter'
        self.network = 'VM Network'
        self.resource_pool = ''
        # self.ova_path = r'C:\Users\adanzun\Downloads\cucm_12.5_vmv13_v1.0.ova'
        self.ova_path = r'C:\Users\adanzun\Downloads\s42700x14_0_4.ova'
        # self.ova_path = r'C:\Users\adanzun\Downloads\s42700x12_7_1_v6.5.ova'
        self.disk_provision = 'thin'
        # self.vm_name = 'C1-CUCM1'
        self.vm_name = 'C1-EXP-C'
        self.deployment = 'CUCM_150_BE6K'
        self.deployment = 'VCS_Small'
        self.datastore_name = 'datastore1'
        self.uuid = ''

    def __repr__(self):
        return f'ESXi=({self.host}:{self.port})'


if __name__ == '__main__':
    exit("Don't Invoke Directly")
