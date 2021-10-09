from pyVmomi import vim, vmodl
from pyVim import connect

esxi_instance = connect.SmartConnectNoSSL(
    host='172.18.9.5',
    user='root',
    pwd='l4bp$$D',
    port=443
)

# ovf_handle = OvfHandler(args.ova_path)

ovf_manager = esxi_instance.content.ovfManager
print(ovf_manager)
print('\n' * 3)

spec_params = vim.OvfManager.CreateImportSpecParams()
print(spec_params)

# vm_obj = ovf_manager.CreateImportSpec(
#         ovf_handle.get_descriptor(), resource_pool, datastore, cisp)
