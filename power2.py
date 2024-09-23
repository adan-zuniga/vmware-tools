import csv
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim
import ssl

# s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
# s.verify_mode = ssl.CERT_NONE
si = SmartConnectNoSSL(host='172.18.9.5', user='root', pwd='l4bp$$D')

with open('vms_to_power_on.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        vm_name = row['VM']
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

        if vm:
            print("Found Virtual Machine:", vm.name)
            # task = vm.PowerOnVM_Task()
            task = vm.PowerOffVM_Task()
            print("Powering on VM...")
            # print(task.info)
            while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
                continue
            if task.info.state == vim.TaskInfo.State.error:
                print(f"Failed to power on VM {vm_name}: {task.info.error}")
        else:
            print("Virtual Machine not found")

# Disconnect from ESXi host or vCenter server
Disconnect(si)