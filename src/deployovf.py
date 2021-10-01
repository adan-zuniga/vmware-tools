from COT.ui import ui
from COT.commands import deploy_esxi
from COT.commands import info

from urllib3 import disable_warnings, exceptions
from pyVim import connect
from pyVmomi import vim, vmodl

from pyvmomi_community_samples.samples.tools import tasks

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


def wait_for_tasks(si, tasks):
    """Given the service instance and tasks, it returns after all the
   tasks are complete
   """
    property_collector = si.content.propertyCollector
    task_list = [str(task) for task in tasks]
    # Create filter
    obj_specs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task)
                 for task in tasks]
    property_spec = vmodl.query.PropertyCollector.PropertySpec(type=vim.Task,
                                                               pathSet=[],
                                                               all=True)
    filter_spec = vmodl.query.PropertyCollector.FilterSpec()
    filter_spec.objectSet = obj_specs
    filter_spec.propSet = [property_spec]
    pcfilter = property_collector.CreateFilter(filter_spec, True)
    try:
        version, state = None, None
        # Loop looking for updates till the state moves to a completed state.
        while task_list:
            update = property_collector.WaitForUpdates(version)
            for filter_set in update.filterSet:
                for obj_set in filter_set.objectSet:
                    task = obj_set.obj
                    for change in obj_set.changeSet:
                        if change.name == 'info':
                            state = change.val.state
                        elif change.name == 'info.state':
                            state = change.val
                        else:
                            continue

                        if not str(task) in task_list:
                            continue

                        if state == vim.TaskInfo.State.success:
                            # Remove task from taskList
                            task_list.remove(str(task))
                        elif state == vim.TaskInfo.State.error:
                            raise task.info.error
            # Move to next version
            version = update.version
    finally:
        if pcfilter:
            pcfilter.Destroy()


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

    obj = None
    for managed_object_ref in container.view:
        if managed_object_ref.name == target_vm:
            obj = managed_object_ref
            break
    container.Destroy()

    vm_object = obj
    cdrom_label = 'CD/DVD drive 1'
    a = vm_object.config
    print(a.cpuAllocation)
    print(a.memmoryAllocation)
    virtual_cdrom_device = None
    for dev in vm_object.config.hardware.device:
        if isinstance(dev, vim.vm.device.VirtualCdrom) and dev.deviceInfo.label == cdrom_label:
            # Connectable startConnected, connected == true
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

    exit()
    dev_changes = [virtual_cd_spec]
    spec = vim.vm.ConfigSpec()
    spec.deviceChange = dev_changes
    task = vm_object.ReconfigVM_Task(spec=spec)
    # wait_for_tasks(esxi_instance, [task])
    tasks.wait_for_tasks(esxi_instance, [task])
    print('CHECK ESXi')


if __name__ == '__main__':
    check_ovx()
    # deploy_to_esxi()
    # update_virtual_machine()