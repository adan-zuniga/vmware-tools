from COT.ui import ui
from COT.commands import deploy_esxi
from COT.commands import info

from urllib3 import disable_warnings, exceptions


disable_warnings(exceptions.InsecureRequestWarning)

api = ui.UI()


def deploy_to_esxi():
    deployer = deploy_esxi.COTDeployESXi(api)
    deployer.datastore = 'datastore1'
    deployer.host = deployer.locator = '172.18.9.5'
    deployer.username = 'root'
    deployer.password = 'l4bp$$D'
    deployer.configuration = 'CER_12000'
    deployer.hypervisor = 'esxi'
    deployer.ovftool_args = '-dm=thin --acceptAllEulas'  # Disk Mode=Thin Provisioning
    deployer.vm_name = 'C1-CER1'
    # deployer.package = rf'C:\Users\adanzun\Downloads\cucm_12.5_vmv13_v1.0.ova'
    deployer.package = rf'C:\Users\adanzun\Downloads\cer_12.5_vmv13_v1.1.ova'
    deployer.network_map = ['eth0=VM Network']
    if deployer.ready_to_run()[0]:
        deployer.run()


def check_ovx():
    checker = info.COTInfo(api)
    ovxs = [r'C:\Users\adanzun\Downloads\cucm_12.5_vmv13_v1.0.ova',
            r'C:\Users\adanzun\Downloads\CUC_12.5_v1.0.ova',
            r'C:\Users\adanzun\Downloads\CUC_12.5_200_user_v1.0.ova',
            r'C:\Users\adanzun\Downloads\cer_12.5_vmv13_v1.1.ova',
            # r"C:\Users\adanzun\OneDrive - CDW\ACE\Phase2\LabNet\Software"
            # r"\OVA's\cucm_im_p_11.5_vmv8_v1.4.ova", r"C:\Users\adanzun\Downloads\cucm_im_p_12.5_vmv13_v1.0.ova"
            ]
    checker.package_list = ovxs
    checker.verbosity = 'brief'
    if checker.ready_to_run()[0]:
        checker.run()


if __name__ == '__main__':
    check_ovx()
    # deploy_to_esxi()