



class ESXi:
    def __init__(self):
        # self.host = '10.89.242.2'
        self.host = '10.0.1.254'
        self.user = 'administrator@vsphere.local'
        # self.password = 'C0c0a123!'
        self.password = 'l4bp$$D!'
        self.port = 443
        self.disable_ssl_verification = True
        self.datacenter_name = 'AZS-DC'
        self.network = 'VM Network'
        self.resource_pool = ''
        # self.ova_path = r"C:\Users\adanzun\OVA\UCSInstall_UCOS_14.0.1.12900-161_80_vmv13_v1.0.ova"
        # self.ova_path = r"C:\Users\adanzun\OVA\UCSInstall_CUP_14.0.1.12901-1_80d_vmv13_v1.0.ova"
        self.ova_path = r"C:\Users\adanzun\OVA\UCSInstall_CUC_14.0.1.12900-69_200_vmv13_v1.0.ova"
        # self.ova_path = r"C:\Users\adanzun\OVA\cucm_15.0_vmv17_v1.2.sha512.ova"
        # self.ova_path = r"C:\Users\adanzun\OVA\s42700x15_0_0.ova"
        # self.ova_path = r"C:\Users\adanzun\OVA\centOSTemplate.ova"
        self.disk_provision = 'thin'
        # self.vm_name = 'C1-CUCM1'
        # self.vm_name = 'C2-IMP'
        self.vm_name = 'Poseidon'
        # self.deployment = 'CUCM_IM_P_5000'
        self.deployment = 'VCS_Small'
        self.datastore_name = 'datastore1'
        self.uuid = ''
        # self.property_mappings = {
        #     'ip4.enable': 'true',
        #     # 'ip4.address': '10.89.242.25',
        #     'ip4.address': '10.0.1.201',
        #     'ip4.netmask': '255.255.255.0',
        #     # 'ip4.gateway': '10.89.242.1',
        #     'ip4.gateway': '10.0.1.1',
        #     'ip6.enable': 'false',
        #     'ip6.address': '',
        #     'ip6.gateway': '',
        #     'dmi.enable': 'false',
        #     'dmi.ip4.address': '192.168.0.100',
        #     'dmi.ip4.netmask': '255.255.255.0',
        #     'dmi.ip6.address': '',
        #     'system.hostname': self.vm_name.lower(),
        #     'domain.name': 'adanzuniga.com',
        #     'ntp.servers': '10.0.1.20',
        #     'default.dns': '10.0.1.20',
        #     'ssh.enabled': 'true',
        #     'webui.enabled': 'true',
        #     'system.timezone': 'America/Chicago',
        #     'ssh.public.key': '',
        #     'ssh.use.standard.port': 'false'
        # }
        # self.property_mappings = {
        #     '1ip0': '10.0.1.130',
        #     '2netmask0': '24',
        #     '3gateway': '10.0.1.1',
        #     '4hostname': 'Ares',
        #     '5dns0': '10.0.1.20',
        #     '6dns1': '8.8.8.8'
        # }
#         self.property_mappings = property_mappings = {
# 	# 'guestinfo.Deployment': 'cups',
# 	# 'guestinfo.isCUCMPub': 'False',
# 	'guestinfo.remote_enabled': 'False',
# 	'guestinfo.os_admin': 'osadmin',
# 	'guestinfo.os_password': 'l4bp$$D',
# 	'guestinfo.security_password': 'l4bp$$D',
# 	'guestinfo.cert_org': 'AZS',
# 	'guestinfo.cert_unit': 'IT',
# 	'guestinfo.cert_loc': 'Chicago',
# 	'guestinfo.cert_state': 'Illinois',
# 	'guestinfo.cert_country': 'United States',
# 	'guestinfo.remote_server_ip': '',
# 	'guestinfo.remote_export_dir': '',
# 	'guestinfo.remote_login_name': '',
# 	'guestinfo.remote_login_password': '',
# 	'guestinfo.smtp_config': 'False',
# 	'guestinfo.smtp': '',
# 	'guestinfo.mtu': '1500',
# 	'guestinfo.DHCP_Enabled': 'False',
# 	'guestinfo.hostname': 'c2-imp2',
# 	'guestinfo.ipaddress': '10.0.1.103',
# 	'guestinfo.netmask': '255.255.255.0',
# 	'guestinfo.Gateway': '10.0.1.1',
# 	'guestinfo.dns_enabled': 'True',
# 	'guestinfo.primary_dns': '10.0.1.20',
# 	'guestinfo.secondary_dns': '',
# 	'guestinfo.domain': 'adanzuniga.com',
# 	'guestinfo.TimeZone': 'America/Chicago',
# 	'guestinfo.imp-domain': 'adanzuniga.com',
# 	'guestinfo.ucm-pub-hostname': 'c2-cucm1',
# 	'guestinfo.ucm-pub-ipaddress': '10.0.1.100',
# }

    def __repr__(self):
        return f'ESXi=({self.host}:{self.port})'


if __name__ == '__main__':
    exit("Don't Invoke Directly")
