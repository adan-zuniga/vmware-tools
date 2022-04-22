from pyVmomi import vim, vmodl
from samples.tools import service_instance
from samples.deploy_ova import OvfHandler
import time
from utilities.crawler import get_dc, get_data_store, get_resource_pool, get_net_mappings
from utilities.home_esxi import ESXi
from utilities.descriptor_analyzer import get_net_ints
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)



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

    ovf__handle.upload_disks(vmware_lease, args.host)

    return True


def parse_descriptor():
    # p = ovf_manager.ParseDescriptor(ovf_handle.get_descriptor(), vim.OvfManager.ParseDescriptorParams(locale='en-US'))
    parse_result = ovf_manager.ParseDescriptor(
        ovfDescriptor=ovf_handle.get_descriptor(),
        pdp=vim.OvfManager.ParseDescriptorParams(
            deploymentOption='VCS_Small',
            locale='en-US')
    )
    properties = []
    for p in parse_result.property:
        match p.id:
            case 'ip4.address':
                v = '10.0.1.200'
            case 'ip4.netmask':
                v = '255.255.255.0'
            case 'ip4.gateway':
                v = '10.0.1.1'
            case 'system.hostname':
                v = args.vm_name
            case 'domain.name':
                v = 'adanzuniga.com'
            case 'ntp.servers':
                v = '10.0.1.20'
            case 'default.dns':
                v = '10.0.1.20'
            case 'system.timezone':
                v = 'America/Chicago'
            case _:
                continue
        properties.append(vim.KeyValue(key=f'.{p.id}.', value=v))

    return properties


if __name__ == '__main__':

    args = ESXi()
    si = service_instance.connect(args)
    dc = get_dc(args, si)
    rp = get_resource_pool(args, si, dc)
    data_store = get_data_store(args, dc)
    network = get_net_mappings(args, dc)
    ovf_handle = OvfHandler(args.ova_path)
    interface = get_net_ints(ovf_handle.get_descriptor())
    ovf_manager = si.content.ovfManager
    prop = parse_descriptor()
    cisp = vim.OvfManager.CreateImportSpecParams(
        diskProvisioning=args.disk_provision,  # diskProvisioning (thin/thick/sparse/etc)
        entityName=args.vm_name,
        # hostSystem='',
        # instantiationOst='',
        # ipAllocationPolicy='',
        # ipProtocol='',
        networkMapping=[vim.OvfManager.NetworkMapping(name=interface, network=network)],
        deploymentOption=args.deployment,
        propertyMapping=prop,
    )
    cisr = ovf_manager.CreateImportSpec(
        ovfDescriptor=ovf_handle.get_descriptor(),
        resourcePool=rp,
        datastore=data_store,
        cisp=cisp
    )
    cisr.importSpec.configSpec.cpuAllocation.reservation = 0
    vm_import_spec = cisr.importSpec
    vm_config_spec = vm_import_spec.configSpec
    vap_config = vm_config_spec.vAppConfig

    new_configSpec = vim.vApp.VmConfigSpec()

    for config in vap_config.property:
        # print(config.info.id)
        operation = 'edit'
        match config.info.id:
            case 'ip4.address':
                propSpec = vim.vApp.PropertySpec()
                propSpec.operation = operation
                propSpec.info = config.info
                propSpec.info.value = '10.0.1.200'
                new_configSpec.property.append(propSpec)
                config.info.value = '10.0.1.200'
                config.info.defaultValue = ''
            case 'ip4.netmask':
                propSpec = vim.vApp.PropertySpec()
                propSpec.operation = operation
                propSpec.info = config.info
                propSpec.info.value = '255.255.255.0'
                new_configSpec.property.append(propSpec)
                config.info.value = '255.255.255.0'
                config.info.defaultValue = ''
            case 'ip4.gateway':
                propSpec = vim.vApp.PropertySpec()
                propSpec.operation = operation
                propSpec.info = config.info
                propSpec.info.value = '10.0.1.1'
                new_configSpec.property.append(propSpec)
                config.info.value = '10.0.1.1'
                config.info.defaultValue = ''
            case 'system.hostname':
                propSpec = vim.vApp.PropertySpec()
                propSpec.operation = operation
                propSpec.info = config.info
                propSpec.info.value = args.vm_name
                new_configSpec.property.append(propSpec)
                config.info.value = args.vm_name
                config.info.defaultValue = ''
            case 'domain.name':
                propSpec = vim.vApp.PropertySpec()
                propSpec.operation = operation
                propSpec.info = config.info
                propSpec.info.value = 'adanzuniga.com'
                new_configSpec.property.append(propSpec)
                config.info.value = 'adanzuniga.com'
                config.info.defaultValue = ''
            case 'ntp.servers':
                propSpec = vim.vApp.PropertySpec()
                propSpec.operation = operation
                propSpec.info = config.info
                propSpec.info.value = '10.0.1.20'
                new_configSpec.property.append(propSpec)
                config.info.value = '10.0.1.20'
                config.info.defaultValue = ''
            case 'default.dns':
                propSpec = vim.vApp.PropertySpec()
                propSpec.operation = operation
                propSpec.info = config.info
                propSpec.info.value = '10.0.1.20'
                new_configSpec.property.append(propSpec)
                config.info.value = '10.0.1.20'
                config.info.defaultValue = ''
            case 'system.timezone':
                propSpec = vim.vApp.PropertySpec()
                propSpec.operation = operation
                propSpec.info = config.info
                propSpec.info.value = 'America/Chicago'
                new_configSpec.property.append(propSpec)
                config.info.value = 'America/Chicago'
                config.info.defaultValue = ''
            case _:
                propSpec = vim.vApp.PropertySpec()
                propSpec.operation = operation
                propSpec.info = config.info
                new_configSpec.property.append(propSpec)

    # cisr.importSpec.configSpec.vAppConfig = new_configSpec
    if cisr.error:
        print("The following errors will prevent import of this OVA:")
        for error in cisr.error:
            print(f'{error}')
            exit()
    else:
        ovf_handle.set_spec(cisr)
        lease = rp.ImportVApp(spec=cisr.importSpec, folder=dc.vmFolder)
        deploy_to_vmware(vmware_lease=lease, ovf__handle=ovf_handle)
