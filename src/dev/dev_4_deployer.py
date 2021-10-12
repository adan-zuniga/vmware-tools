from samples.tools import cli, service_instance
from utilities.virtualtemplates import OvfHandler
import xmltodict


def list_deployment_types(deployment_list):
    print(' Deployments '.center(180, "#"))
    for deployment in deployment_list:
        print(deployment['@ovf:id'].center(100, '_'))
        print(deployment['@ovf:id'])
        print(deployment['Label'])
        print(deployment['Description'], '\n' * 2)


def list_net_interfaces(net_section):
    print(' vNICs '.center(180, "#"))
    net_dict = (dict(net_section))
    net_dict['Network'] = dict(net_dict.pop('Network'))
    network = net_dict['Network']
    interface = network['@ovf:name']
    interface_description = network['Description']
    print(interface)
    print(interface_description)


def list_vir_hardware(vh):
    print(' VirtualHardware '.center(180, "#"))
    print(vh['Info'])
    print(dict(vh['System']))
    # print(dict(vh['vmw:Config']))
    # print(dict(vh['vmw:ExtraConfig']))
    vhs = [dict(h) for h in vh['Item']]
    for item in vhs:
        print(item)
        print(item.get('@ovf:configuration'))
        print(item.get('rasd:AllocationUnits'))
        print(item.get('rasd:ElementName'))
        print(item.get('rasd:Reservation'))
        print(item.get('rasd:ResourceType'))
        print(item.get('rasd:VirtualQuantity'))
        # print(*deployment_hardware.keys())


def list_virtual_system(vir_system):
    print(' GuestOS '.center(180, "#"))
    operating_system = dict(vir_system['OperatingSystemSection'])
    print(operating_system.get('Description'))
    print(operating_system['@vmw:osType'])
    print(operating_system.get('@ovf:version'))
    vh = dict(vir_system['VirtualHardwareSection'])
    list_vir_hardware(vh)


# ova_path = r'C:\Users\adanzun\OneDrive - CDW\Customers\ULTA\Software\CUC_12.5_v1.0.ova'
ova_path = r'C:\Users\adanzun\Downloads\s42700x12_7_1_v6.5.ova'
# ova_path = r'C:\Users\adanzun\OneDrive - CDW\Customers\Crystal Clinic\Shared\CUACA_SV_14.0.1.10.zip'
ovf_handle = OvfHandler(ovafile=ova_path)

ovf_xml = ovf_handle.get_descriptor()
ova_descriptor_obj = xmltodict.parse(ovf_xml)
envelope = ova_descriptor_obj['Envelope']
# r = envelope['References']

configurations = [dict(c) for c in envelope['DeploymentOptionSection']['Configuration']]
list_deployment_types(configurations)

network_section = envelope['NetworkSection']
list_net_interfaces(network_section)


virtual_system = dict(envelope['VirtualSystem'])
list_virtual_system(virtual_system)
