from pyVmomi import vim, vmodl
from pyVim import connect

esxi_instance = connect.SmartConnectNoSSL(
    host='172.18.9.5',
    user='root',
    pwd='l4bp$$D',
    port=443
)

p = vim.OvfManager.CreateImportSpecParams()
print(d := esxi_instance.content.ovfManager)
print(p)
