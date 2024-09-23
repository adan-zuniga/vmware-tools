from pyVmomi import vim, vmodl
from samples.tools import service_instance
from samples.deploy_ova import OvfHandler
import time
from src.utilities.crawler import get_dc, get_data_store, get_resource_pool, get_net_mappings, get_obj
from src.utilities.home_esxi import ESXi
from src.utilities.descriptor_analyzer import get_net_ints
from src.utilities import get_vm_by_name
from samples.tools import tasks




if __name__ == '__main__':

    args = ESXi()

    esxi_instance = service_instance.connect(args)
    content = esxi_instance.RetrieveContent()
    vm = get_vm_by_name(esxi_instance, args.vm_name)
    # print(vm.name)
    # print(vm.config.vAppConfig)
    # vmn = get_obj(content, [vim.VirtualMachine], 'EXP')

    # config = vm.config
    # print(vmn.name)
    #
    print(vars())
    exit()
    configSpec = vim.vApp.VmConfigSpec()

    for prop in config.vAppConfig.property:
        print(prop)


    # print(spec)