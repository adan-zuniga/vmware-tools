from utilities.home_esxi import ESXi as args
from samples.tools import service_instance
from utilities.crawler import get_dc

esxi_instance = args()
print(esxi_instance)

si = service_instance.connect(esxi_instance)
dc = get_dc(esxi_instance, si)
print(dc.name)
