# from samples.tools import cli, service_instance
from utilities.virtualtemplates import OvfHandler
import xml.etree.ElementTree as ET
import xmltodict

# parser = cli.Parser()
# args = parser.get_args()

ova_path = r'C:\Users\adanzun\OneDrive - CDW\Customers\ULTA\Software\CUC_12.5_v1.0.ova'
ovf_handle = OvfHandler(ovafile=ova_path)

# for v in vars(ovf_handle).items():
#     print(v)

ovf_xml = ovf_handle.get_descriptor()
print(ovf_xml)

xml_obj = xmltodict.parse(ovf_xml)
a = ''

# root = ET.fromstring(ovf_xml)
#
# print(root)
#
# for child in root:
#     print(child.tag, child.attrib)
# #
# print(vars(ovf_handle.handle))
# print(vars(ovf_handle.tarfile))
