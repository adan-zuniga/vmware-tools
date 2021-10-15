from pyVim import connect
from pyVmomi import vim, vmodl
from samples.tools import tasks


def update_virtual_machine():

    target_vm = 'C1-CER1'
    esxi_instance = connect.SmartConnectNoSSL(
        host='172.18.9.5',
        user='root',
        pwd='l4bp$$D',
        port=443
    )

    content = esxi_instance.RetrieveContent()
    folder = content.rootFolder  # starting point to look into
    view_type = [vim.VirtualMachine]  # object types to look for
    recursive = True  # whether we should look into it recursively
    container = content.viewManager.CreateContainerView(folder, view_type, recursive)

    vm_obj = None
    for managed_object_ref in container.view:
        if managed_object_ref.name == target_vm:
            vm_obj = managed_object_ref
            break
    container.Destroy()

    vm_object = vm_obj
    cdrom_label = 'CD/DVD drive 1'
    # vm_config = vm_object.config
    # print(vm_config.cpuAllocation)
    # print(vm_config.memmoryAllocation)
    virtual_cdrom_device = None
    for dev in vm_object.config.hardware.device:
        if isinstance(dev, vim.vm.device.VirtualCdrom) and dev.deviceInfo.label == cdrom_label:
            virtual_cdrom_device = dev

    virtual_cd_spec = vim.vm.device.VirtualDeviceSpec()
    virtual_cd_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
    virtual_cd_spec.device = vim.vm.device.VirtualCdrom()
    virtual_cd_spec.device.controllerKey = virtual_cdrom_device.controllerKey
    virtual_cd_spec.device.key = virtual_cdrom_device.key
    virtual_cd_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    # if full_path_to_iso is provided it will mount the iso

    virtual_cd_spec.device.backing = vim.vm.device.VirtualCdrom.IsoBackingInfo()
    virtual_cd_spec.device.backing.fileName = '[datastore1] ISOs/UC/Bootable_UCSInstall_CER_12.5.1.23900-19.sgn.iso'
    virtual_cd_spec.device.connectable.connected = True
    virtual_cd_spec.device.connectable.startConnected = True

    dev_changes = [virtual_cd_spec]
    spec = vim.vm.ConfigSpec()
    spec.deviceChange = dev_changes
    task = vm_object.ReconfigVM_Task(spec=spec)
    tasks.wait_for_tasks(esxi_instance, [task])
    print('CHECK ESXi')


if __name__ == '__main__':
    update_virtual_machine()