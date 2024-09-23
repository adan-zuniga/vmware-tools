from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim
import ssl

# s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
# s.verify_mode = ssl.CERT_NONE
# si = SmartConnect(host="172.18.9.5", user="root", pwd="l4bp$$D", sslContext=s)
# si = SmartConnect(host="172.18.9.5", user="root", pwd="l4bp$$D", port=443, disableSslCertValidation=True)
si = SmartConnectNoSSL(host='172.18.9.5', user='root', pwd='l4bp$$D')

# vm_name = "C1-CUCM2"
# # content = si.RetrieveContent()
# # vm = None
# # for child in content.rootFolder.childEntity:
# #     if hasattr(child, 'vmFolder'):
# #         vm_folder = child.vmFolder
# #         vm_list = vm_folder.childEntity
# #         for virtual_machine in vm_list:
# #             if virtual_machine.name == vm_name:
# #                 vm = virtual_machine
# #                 break
# #
# # if vm:
# #     print("Found Virtual Machine:", vm.name)
# #     task = vm.PowerOnVM_Task()
# #     print("Powering on VM...")
# #     print(task.info)
# # else:
# #     print("Virtual Machine not found")
#
#
# # Disconnect from ESXi host or vCenter server
# Disconnect(si)


vm_names = ['C1-CUCM2']
content = si.RetrieveContent()
vm = None
for child in content.rootFolder.childEntity:
    if hasattr(child, 'vmFolder'):
        vm_folder = child.vmFolder
        vm_list = vm_folder.childEntity
        for virtual_machine in vm_list:
            if virtual_machine.name == vm_name:
                vm = virtual_machine
                break
#
# if vm:
#     print("Found Virtual Machine:", vm.name)
#     task = vm.PowerOnVM_Task()
#     print("Powering on VM...")
#     print(task.info)
# else:
#     print("Virtual Machine not found")


# Disconnect from ESXi host or vCenter server
Disconnect(si)





from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnectNoSSL, Disconnect
import csv

# Connect to ESXi host or vCenter server
si = SmartConnectNoSSL(host='172.18.9.5', user='root', pwd='l4bp$$D')

# Obtain the content and root folder objects
content = si.RetrieveContent()
root_folder = content.rootFolder

# Open the input CSV file and read the VM names
# with open('vm_list.csv', 'r') as csvfile:
#     reader = csv.reader(csvfile)
#     vm_names = [row[0] for row in reader]
vm_names = ['C1-CUCM2']

# Power on the specified VMs
for vm_name in vm_names:
    vm = content.searchIndex.FindByDnsName(None, vm_name, True)
    if vm is None:
        print(f"VM with name {vm_name} not found")
    else:
        print(f"Powering on VM {vm_name}")
        task = vm.PowerOnVM_Task()
        while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
            continue
        if task.info.state == vim.TaskInfo.State.error:
            print(f"Failed to power on VM {vm_name}: {task.info.error}")

# Disconnect from ESXi host or vCenter server
Disconnect(si)
