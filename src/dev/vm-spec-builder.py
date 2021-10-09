from pyVmomi import vim, vmodl

# hostSystem, networkMapping, resourceMapping
cisp = vim.OvfManager.CreateImportSpecParams(deploymentOption='', entityName='The VM Name',
                                             diskProvisioning='thick')

# print(cisp)

# vp = vmodl.DynamicProperty()

# print(vp)

print(vim.OvfManager.NetworkMapping())
print(vim.KeyValue())