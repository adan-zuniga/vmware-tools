from pprint import pprint

from pyVmomi import vim, vmodl
from samples.tools import service_instance
from samples.deploy_ova import OvfHandler
from samples.tools import tasks

from src.utilities.crawler import get_dc, get_data_store, get_resource_pool, get_net_mappings
from src.utilities.home_esxi import ESXi
from src.utilities.descriptor_analyzer import get_net_ints
from src.utilities import deploy_to_vmware
from src.utilities import get_vm_by_name


def create_property_mappings_dict(import_spec):
    properties =import_spec.importSpec.configSpec.vAppConfig.property
    property_dict = {p.info.id: p.info.value for p in properties}
    pprint(property_dict, sort_dicts=False)


def update_vap_config(isr, operation='edit'):
    """Update the vApp config contained at: cisr.importSpec.configSpec.vAppConfig

    Written on 7/10/2024

    Not Tested yet.

    """
    with open('before.txt', mode='w') as before_file:
        before_file.write(str(isr.importSpec.configSpec.vAppConfig))

    configSpec = vim.vApp.VmConfigSpec()

    for prop in isr.importSpec.configSpec.vAppConfig.property:
        new_value = args.property_mappings.get(prop.info.id)
        propSpec = vim.vApp.PropertySpec()
        propSpec.operation = operation
        propSpec.info = prop.info
        propSpec.info.value = new_value
        configSpec.property.append(propSpec)
    new_prod_spec = vim.vApp.ProductSpec()
    configSpec.product = isr.importSpec.configSpec.vAppConfig.product

    with open('after.txt', mode='w') as after_file:
        after_file.write(str(configSpec))


    return configSpec



if __name__ == '__main__':

    args = ESXi()

    esxi_instance = service_instance.connect(args)

    dc = get_dc(args, esxi_instance)
    rp = get_resource_pool(args, esxi_instance, dc)
    data_store = get_data_store(args, dc)
    network = get_net_mappings(args, dc)

    app_ova = OvfHandler(args.ova_path)

    ova_xml_descriptor = app_ova.get_descriptor()
    interface = get_net_ints(ova_xml_descriptor)

    ovf_manager = esxi_instance.content.ovfManager


    cisp = vim.OvfManager.CreateImportSpecParams()
        # diskProvisioning=args.disk_provision,  # diskProvisioning (thin/thick/sparse/etc)
        # entityName=args.vm_name,
        # networkMapping=[vim.OvfManager.NetworkMapping(name=interface, network=network)],
        # deploymentOption=args.deployment,
        # propertyMapping=[vim.KeyValue(key=f'{k}', value=v) for k, v in args.property_mappings.items()],
    # )
    cisp.diskProvisioning = args.disk_provision
    cisp.entityName = args.vm_name

    nma = vim.OvfManager.NetworkMapping.Array()
    nm = vim.OvfManager.NetworkMapping(name=interface, network=network)
    nma.append(nm)
    cisp.networkMapping = nma
    # cisp.networkMapping=[vim.OvfManager.NetworkMapping(name=interface, network=network)],
    # cisp.deploymentOption = args.deployment



    cisr = ovf_manager.CreateImportSpec(
        ovfDescriptor=ova_xml_descriptor,
        resourcePool=rp,
        datastore=data_store,
        cisp=cisp
    )
    # print(cisr.importSpec.configSpec.vAppConfig)
    # for prop in cisr.importSpec.configSpec:
    updated_vAppSection = update_vap_config(cisr, operation='add')
    # cisr.importSpec.configSpec.vAppConfig = updated_vAppSection
    # for prop in cisr.importSpec.configSpec.vAppConfig.property:
    #     prop.operation = vim.option.ArrayUpdateSpec.Operation.add

    cisr.importSpec.configSpec.vAppConfigRemoved = False
    edit_vAppSection = updated_vAppSection
    for p in edit_vAppSection.property:
        p.operation = 'add'
    edit_vAppSection.product.operation = 'add'

    # print(cisr)

    deploy_to_vmware(cisr, rp, dc, app_ova, args)
    exit()
    vm = get_vm_by_name(esxi_instance, args.vm_name)

    cspec = vim.vm.ConfigSpec()
    config = vm.config
    # configSpec = vim.vApp.VmConfigSpec()
    cspec.vAppConfig = updated_vAppSection
    task = vm.ReconfigVM_Task(spec=cspec)
    tasks.wait_for_tasks(esxi_instance, [task])
    print('CHECK ESXi')
    # reconfigure_vm(cluster, server.hostname, cspec)