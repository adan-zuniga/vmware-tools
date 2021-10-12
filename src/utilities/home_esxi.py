class ESXi:
    def __init__(self):
        self.host = '172.18.9.5'
        self.user = 'root'
        self.password = 'l4bp$$D'
        self.port = 443
        self.disable_ssl_verification = True
        self.datacenter_name = ''
        self.resource_pool = ''
        self.datastore_name = ''
        self.ova_path = ''

    def __repr__(self):
        return f'ESXi=({self.host}:{self.port})'


if __name__ == '__main__':
    exit("Don't Invoke Directly")