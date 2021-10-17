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
        self.ova_path = r'C:\Users\adanzun\OneDrive - CDW\Customers\ULTA\Software\CUC_12.5_v1.0.ova'
        self.disk_provision = 'thin'
        self.vm_name = '10-17-2021 UCXN'
        self.deployment = 'CUC-Overlay-1'
        self.datastore_name = 'datastore1'

    def __repr__(self):
        return f'ESXi=({self.host}:{self.port})'


if __name__ == '__main__':
    exit("Don't Invoke Directly")
