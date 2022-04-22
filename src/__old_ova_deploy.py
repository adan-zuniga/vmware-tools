from pyVmomi import vim, vmodl
from samples.tools import service_instance
from samples.deploy_ova import OvfHandler
import time
from utilities.crawler import get_dc, get_data_store, get_resource_pool, get_net_mappings
from utilities.home_esxi import ESXi
from utilities.descriptor_analyzer import get_net_ints


def deploy_to_vmware(vmware_lease, ovf__handle):

    while vmware_lease.state == vim.HttpNfcLease.State.initializing:
        print('Waiting for lease to be ready...')
        time.sleep(1)

    if vmware_lease.state == vim.HttpNfcLease.State.error:
        print(f'Lease error: {vmware_lease.error}')
        return 1
    if vmware_lease.state == vim.HttpNfcLease.State.done:
        return 0

    print('Starting deploy...')
    return ovf__handle.upload_disks(vmware_lease, args.host)


args = ESXi()
si = service_instance.connect(args)
dc = get_dc(args, si)
print(dc.name)
print(dc.vmFolder)

rp = get_resource_pool(args, si, dc)
print(rp.name)

data_store = get_data_store(args, dc)
print(data_store.name)

network = get_net_mappings(args, dc)
print(network.name)

ovf_handle = OvfHandler(args.ova_path)
interface = get_net_ints(ovf_handle.get_descriptor())

ovf_manager = si.content.ovfManager
cisp = vim.OvfManager.CreateImportSpecParams(
    deploymentOption=args.deployment,
    entityName=args.vm_name,
    diskProvisioning=args.disk_provision, # diskProvisioning (thin/thick/sparse/etc)
    # hostSystem='',
    networkMapping=[vim.OvfManager.NetworkMapping(name=interface, network=network)]
)

cisr = ovf_manager.CreateImportSpec(
    ovfDescriptor=ovf_handle.get_descriptor(),
    resourcePool=rp,
    datastore=data_store,
    cisp=cisp)

vm_import_spec = cisr.importSpec
vm_config_spec = vm_import_spec.configSpec

cd_index = 0
# cd_specs = None
for c, d in enumerate(vm_config_spec.deviceChange):

    if isinstance(d.device, vim.vm.device.VirtualCdrom):
        print(d)
        # d.device.backing = vim.vm.device.VirtualCdrom.IsoBackingInfo()
        print('#' * 130)

        # new_cd = vim.vm.device.VirtualDeviceSpec()
        # new_cd.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
        # new_cd.device = device = vim.vm.device.VirtualCdrom()
        # new_cd.device.controllerKey = d.device.controllerKey
        # new_cd.device.key = d.device.key
        # new_cd.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        # new_cd.device.backing = vim.vm.device.VirtualCdrom.IsoBackingInfo()
        # new_cd.device.backing.fileName = '[datastore1] ISOs/UC/Bootable_UCSInstall_UCOS_12.5.1.14900-63.sgn.iso'
        # new_cd.device.connectable.connected = True
        # new_cd.device.connectable.startConnected = True
        # print(new_cd)
        # d = new_cd
        cd_index = c
        vm_config_spec.deviceChange[c].device.backing = vim.vm.device.VirtualCdrom.IsoBackingInfo()
        vm_config_spec.deviceChange[c].device.backing.fileName = \
            '[datastore1] ISOs/UC/Bootable_UCSInstall_UCOS_12.5.1.14900-63.sgn.iso'
        vm_config_spec.deviceChange[c].device.connectable.connected = True
        vm_config_spec.deviceChange[c].device.connectable.startConnected = True
        print(vm_config_spec.deviceChange[c])
        print('#' * 130)
    if isinstance(d.device, vim.vm.device.VirtualFloppy):
        vm_config_spec.deviceChange[c].device.backing = vim.vm.device.VirtualFloppy.ImageBackingInfo()
        vm_config_spec.deviceChange[c].device.backing.fileName = \
            f'[datastore1] AF/125/{args.vm_name.lower()}.vfd'
        vm_config_spec.deviceChange[c].device.connectable.connected = True
        vm_config_spec.deviceChange[c].device.connectable.startConnected = True
        print(vm_config_spec.deviceChange[c])
        print(d.device, end='\n' * 3)

    # else:
    #     print(type(d.device))

        # cd_specs = new_cd

# vm_config_spec.deviceChange[cd_index].device.backing = vim.vm.device.VirtualCdrom.IsoBackingInfo()
# vm_config_spec.deviceChange[cd_index].device.backing.fileName = \
#     '[datastore1] ISOs/UC/Bootable_UCSInstall_UCOS_12.5.1.14900-63.sgn.iso'
# vm_config_spec.deviceChange[cd_index].device.connectable.connected = True
# vm_config_spec.deviceChange[cd_index].device.connectable.startConnected = True


# vm_config_spec.deviceChange[cd_index] = cd_specs
        # print(d.device)
    # elif isinstance(d.device, vim.vm.device.VirtualFloppy):
    #     print(d.device)
    # elif isinstance(d.device, vim.vm.device.VirtualDisk):
    #     print(d.device)
# These errors might be handleable by supporting the parameters in
if cisr.error:
    print("The following errors will prevent import of this OVA:")
    for error in cisr.error:
        print(f'{error}')
        exit()
else:
    ovf_handle.set_spec(cisr)

    lease = rp.ImportVApp(spec=cisr.importSpec, folder=dc.vmFolder)
    deploy_to_vmware(vmware_lease=lease, ovf__handle=ovf_handle)
