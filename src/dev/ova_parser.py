from samples.deploy_ova import OvfHandler
from collections import defaultdict
import untangle


resource_dict = {
    3: 'vCPU',
    4: 'vRAM',
    5: 'IDE Controller',
    6: 'Parallel SCSI HBA',
    10: 'Ethernet Adapter',
    14: 'Floppy Drive',
    15: 'CD Drive',
    17: 'vDisk Drive',
    23: 'USB Controller',
    24: 'Graphics controller'
}


def list_deployment_types(deployment_list, hw_dict_in):
    # deployment_dict =
    for deployment in deployment_list:
        deployment_type = deployment['ovf:id']
        print(deployment_type.center(120, '#'))
        resources = hw_dict_in[deployment_type]
        for resource in resources:
            print(resource)
        print(deployment.Label.cdata)
        print(deployment.Description.cdata)


def list_net_interfaces(net_section):
    interface = net_section.Network['ovf:name']
    net_description = net_section.Network.Description.cdata
    print(interface)
    print(net_description)


def is_global_resource(o, resource_attribute):
    resource_value = getattr(o, resource_attribute, None)
    if resource_value is not None:
        # print(resource_value.cdata)
        return resource_value.cdata
    else:
        # print('\tAllocation Units')
        return ''


def list_vir_hardware(vh):
    virtual_hardware_dict = defaultdict(list)
    # print(virtual_hardware_dict)
    for item in vh.Item:
        deployment_type = item['ovf:configuration'] or 'Shared'
        al_units = is_global_resource(item, 'rasd_AllocationUnits')
        vh_kind = item.rasd_ElementName.cdata
        reservation = is_global_resource(item, 'rasd_Reservation')
        vh_quantity = is_global_resource(item, 'rasd_VirtualQuantity')
        rt = item.rasd_ResourceType.cdata
        # print(resource_dict.get(int(rt), f'Add {rt} to DICT'))
        virtual_hardware_dict[deployment_type].append(dict
                                                      (vhard=resource_dict.get(int(rt), rt),
                                                       units=al_units,
                                                       vh_descr=vh_kind,
                                                       reservation=reservation,
                                                       vh_quantity=vh_quantity,
                                                       ))

    # print(dict(virtual_hardware_dict))
    # for d in virtual_hardware_dict:
    #     print(d)
    #     for e in virtual_hardware_dict[d]:
    #         print('\t' * 2, e)
    return dict(virtual_hardware_dict)


def list_os(os_info):
    ovf_version = os_info['ovf:version']
    os_type = os_info['vmw:osType']
    # os_info = os_info.Description.cdata
    # vars(os_info)
    print(ovf_version)
    # print(os_info)
    print(os_type)
    # list_vir_hardware(vir_system.VirtualHardwareSection)
    # return vir_system.VirtualHardwareSection


# ova_path = r'C:\Users\adanzun\Downloads\cucm_12.5_vmv13_v1.0.ova'
# ova_path = r'C:\Users\adanzun\OneDrive - CDW\Customers\Crystal Clinic\cucm_14.0_vmv13_v1.1.ova'
# ova_path = r'C:\Users\adanzun\OneDrive - CDW\Customers\ULTA\cucm_10.5_vmv8_v2.0.ova'
# ova_path = r'C:\Users\adanzun\Downloads\s42700x12_7_1_v6.5.ova'
# ova_path = r'C:\Users\adanzun\Downloads\s42700x14_0_4.ova'
# ova_path = r'C:\Users\adanzun\Downloads\cucm_14.0_vmv13_v1.1.ova'
ova_path = r'C:\Users\adanzun\Downloads\cer_14.0_vmv13_v1.0.ova'
ovf_handle = OvfHandler(ovafile=ova_path)

ovf_xml = ovf_handle.get_descriptor()
ova_descriptor_obj = untangle.parse(ovf_xml)
envelope = ova_descriptor_obj.Envelope
# print(envelope.VirtualSystem.ProductSection.Property)
# Virtual System
virtual_system = envelope.VirtualSystem
ovf_id = virtual_system['ovf:id']
print(ovf_id)
# virtual_hardware = list_os(virtual_system)
list_os(virtual_system.OperatingSystemSection)
product_info = virtual_system.ProductSection

virtual_hardware = virtual_system.VirtualHardwareSection
hw_dict = list_vir_hardware(virtual_hardware)

# Deployment Types
configurations = envelope.DeploymentOptionSection.Configuration
list_deployment_types(configurations, hw_dict)

# Networks
# network_section = envelope.NetworkSection
# list_net_interfaces(network_section)

