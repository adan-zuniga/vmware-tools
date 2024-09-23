"""Customization of Ryan Mullins' deployment script"""

from src.utilities.crawler import get_obj
from src.utilities.home_esxi import ESXi
from samples.tools import service_instance
from pyVmomi import vim, vmodl

args = ESXi()

esxi_instance = service_instance.connect(args)
content = esxi_instance.RetrieveContent()


# """
# Verify our datacenter is ok
# """
# dc_obj = get_obj(content, [vim.Datacenter], args.datacenter_name)
# if not dc_obj:
#     raise SystemExit()
#
# print(dc_obj.name)
#
# cluster_obj = get_obj(content, [vim.ClusterComputeResource])
# if not cluster_obj:
#     raise Exception(f' cluster_obj is {cluster_obj}')
# print(cluster_obj)
c = get_obj(content)