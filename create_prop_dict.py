from pprint import pprint

from pyVmomi import vim, vmodl
from samples.tools import service_instance
from samples.deploy_ova import OvfHandler
import time
from src.utilities.crawler import get_dc, get_data_store, get_resource_pool, get_net_mappings
from src.utilities.home_esxi import ESXi
from src.utilities.descriptor_analyzer import get_net_ints



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

    parse_result = ovf_manager.ParseDescriptor(
        ovfDescriptor=ova_xml_descriptor,
        pdp=vim.OvfManager.ParseDescriptorParams(
            # deploymentOption=args.deployment,
            # locale='en-US'
        )
    )
    # print(parse_result)
    # exit()
    prop_dict = {}
    for p in parse_result.property:
        # k = f'{p.classId}.{p.id}.{p.instanceId}'
        # print(f' --prop:{p.id}={p.defaultValue}^')
        # print(f'{p.description}\n')
        # v = f'{p.defaultValue}'
        # prop_dict[k] = v
        pprint(p)
        print()
    # pprint(prop_dict, sort_dicts=False)
