from pyVmomi import vim, vmodl
from samples.tools import service_instance
from samples.deploy_ova import OvfHandler
import time
from utilities.crawler import get_dc, get_data_store, get_resource_pool, get_net_mappings
from utilities.home_esxi import ESXi
from src.utilities import deploy_to_vmware
from utilities.descriptor_analyzer import get_net_ints


if __name__ == '__main__':

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

    for c, d in enumerate(vm_config_spec.deviceChange):

        if isinstance(d.device, vim.vm.device.VirtualCdrom):
            print(d)
            print('#' * 130)

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
                f'[datastore1] AF/125/{args.vm_name.lower()}.flp'
            vm_config_spec.deviceChange[c].device.connectable.connected = True
            vm_config_spec.deviceChange[c].device.connectable.startConnected = True
            print(vm_config_spec.deviceChange[c])
            print(d.device, end='\n' * 3)



    deploy_to_vmware(cisr, rp, dc, ovf_handle, args)
