from pyVmomi import vim, vmodl
from samples.tools import service_instance
from samples.deploy_ova import OvfHandler
import time
from src.utilities.crawler import get_dc, get_data_store, get_resource_pool, get_net_mappings
from src.utilities.home_esxi import ESXi
from src.utilities.descriptor_analyzer import get_net_ints
from src.utilities import get_vm_by_name
from samples.tools import tasks


def generate_new_configSpec(vap__config):
    new_configSpec = vim.vApp.VmConfigSpec()

    for config in vap__config.property:

        propSpec = config

        if propSpec.info.userConfigurable:
            v = args.property_mappings.get(config.info.id, '')

            propSpec.operation = vim.option.ArrayUpdateSpec.Operation.edit
            propSpec.info.value = v
            new_configSpec.property.append(propSpec)

    return new_configSpec


# def set_vapp_properties(pr):
#     properties = []
#
#     for p in pr.property:
#         if p.userConfigurable:
#             v = property_mappings.get(p.id, '')
#
#         properties.append(vim.KeyValue(key=f'.{p.id}.', value=v))
#
#     return properties


if __name__ == '__main__':

    args = ESXi()

    esxi_instance = service_instance.connect(args)

    vm = get_vm_by_name(esxi_instance, args.vm_name)

    # Update any configuration we need
    cspec = vim.vm.ConfigSpec()


    dc = get_dc(args, esxi_instance)
    rp = get_resource_pool(args, esxi_instance, dc)
    data_store = get_data_store(args, dc)
    network = get_net_mappings(args, dc)

    app_ova = OvfHandler(args.ova_path)

    ova_xml_descriptor = app_ova.get_descriptor()
    interface = get_net_ints(ova_xml_descriptor)

    ovf_manager = esxi_instance.content.ovfManager

    parse_result = ovf_manager.ParseDescriptor(
        ovfDescriptor=ova_xml_descriptor,
        pdp=vim.OvfManager.ParseDescriptorParams(
            deploymentOption=args.deployment,
            # locale='en-US'
        )
    )

    # updated_v_app_prop = set_vapp_properties(parse_result)

    # ncs = generate_new_configSpec()

    cisp = vim.OvfManager.CreateImportSpecParams(
        diskProvisioning=args.disk_provision,  # diskProvisioning (thin/thick/sparse/etc)
        entityName=args.vm_name,

        networkMapping=vim.OvfManager.NetworkMapping.Array(vim.OvfManager.NetworkMapping(name=interface, network=network)),
        deploymentOption=args.deployment,
        # propertyMapping=[vim.KeyValue(key=k, value=v) for k, v in args.property_mappings.items()],
    )

    # cisp.vAppConfig = ncs

    cisr = ovf_manager.CreateImportSpec(
        ovfDescriptor=ova_xml_descriptor,
        resourcePool=rp,
        datastore=data_store,
        cisp=cisp
    )

    # cisr.importSpec.configSpec.cpuAllocation.reservation = 0
    # vm_import_spec = cisr.importSpec
    # vm_config_spec = vm_import_spec.configSpec
    vap_config = cisr.importSpec.configSpec.vAppConfig


    spec = vim.vm.ConfigSpec()
    vAppConfig = generate_new_configSpec(vap_config)

    # spec.vAppConfig = vAppConfig
    spec.vAppConfig = vap_config
    for config in spec.vAppConfig.property:
        if config.info.userConfigurable:
            config.operation = vim.option.ArrayUpdateSpec.Operation.add

    print(spec)

    # vm.config.vAppConfig = spec.vAppConfig



    # task = vm.ReconfigVM_Task(spec=spec)
    # tasks.wait_for_tasks(esxi_instance, [task])
    # print('CHECK ESXi')



