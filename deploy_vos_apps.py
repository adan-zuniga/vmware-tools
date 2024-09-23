from pyVmomi import vim, vmodl
from samples.tools import service_instance
from samples.deploy_ova import OvfHandler
import time
from src.utilities.crawler import get_dc, get_data_store, get_resource_pool, get_net_mappings
from src.utilities.home_esxi import ESXi
from src.utilities.descriptor_analyzer import get_net_ints
from src.utilities import deploy_to_vmware
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def generate_new_configSpec():
    new_configSpec = vim.vApp.VmConfigSpec()

    for config in vap_config.property:

        # operation = 'edit'

        match config.info.id:
            case 'guestinfo.Deployment':
                v = 'S'
            case 'guestinfo.isCUCMPub':
                v = 'True'
            case 'guestinfo.remote_enabled':
                v = 'False'
            case 'guestinfo.os_admin':
                v = 'osadmin'
            case 'guestinfo.os_password':
                v = 'l4bp$$D'
            case 'guestinfo.security_password':
                v = 'l4bp$$D'
            case 'guestinfo.appln_user':
                v = 'appadmin'
            case 'guestinfo.appln_pass':
                v = 'l4bp$$D'
            case 'guestinfo.cert_org':
                v = 'AZS'
            case 'guestinfo.cert_unit':
                v = 'IT'
            case 'guestinfo.cert_loc':
                v = 'Chicago'
            case 'guestinfo.cert_state':
                v = 'Illinois'
            case 'guestinfo.cert_country':
                v = 'United States'
                # case 'guestinfo.remote_server_ip':
                # case 'guestinfo.remote_export_dir':
                # case 'guestinfo.remote_login_name':
                # case 'guestinfo.remote_login_password':
            case 'guestinfo.dynamic_cluster_config':
                v = 'True'
            case 'guestinfo.cluster_config_timer':
                v = '3'
            case 'guestinfo.smtp_config':
                v = 'False'
                # case 'guestinfo.smtp':
                # case 'guestinfo.mtu':
            case 'guestinfo.DHCP_Enabled':
                v = 'False'
            case 'guestinfo.hostname':
                v = 'c2-cucm1'
            case 'guestinfo.ipaddress':
                v = '10.0.1.100'
            case 'guestinfo.netmask':
                v = '255.255.255.0'
            case 'guestinfo.Gateway':
                v = '10.0.1.100'
            case 'guestinfo.dns_enabled':
                v = 'True'
            case 'guestinfo.primary_dns':
                v = '10.0.1.20'
                # case 'guestinfo.secondary_dns':
            case 'guestinfo.domain':
                v = 'adanzuniga.com'
            case 'guestinfo.TimeZone':
                v = 'America/Chicago'
            case 'guestinfo.ntp1':
                v = '10.0.1.20'
                # case 'guestinfo.ntp2':
                # case 'guestinfo.ntp3':
                # case 'guestinfo.ntp4':
                # case 'guestinfo.ntp5':
            case 'guestinfo.ucm-sub1-hostname':
                v = 'c2-cucm2'
            case 'guestinfo.ucm-sub1-ipaddress':
                v = '10.0.1.101'
                # case 'guestinfo.ucm-sub2-hostname':
                # case 'guestinfo.ucm-sub2-ipaddress':
                # case 'guestinfo.ucm-sub3-hostname':
                # case 'guestinfo.ucm-sub3-ipaddress':
                # case 'guestinfo.ucm-sub4-hostname':
                # case 'guestinfo.ucm-sub4-ipaddress':
                # case 'guestinfo.ucm-sub5-hostname':
                # case 'guestinfo.ucm-sub5-ipaddress':
            case 'guestinfo.imp-domain':
                v = 'adanzuniga.com'
            case 'guestinfo.imp-sub1-hostname':
                v = 'c2-imp'
            case 'guestinfo.imp-sub1-ipaddress':
                v = '10.0.1.102'
                # case 'guestinfo.imp-sub2-hostname':
                # case 'guestinfo.imp-sub2-ipaddress':
                # case 'guestinfo.imp-sub3-hostname':
                # case 'guestinfo.imp-sub3-ipaddress':
                # case 'guestinfo.imp-sub4-hostname':
                # case 'guestinfo.imp-sub4-ipaddress':
                # case 'guestinfo.imp-sub5-hostname':
                # case 'guestinfo.imp-sub5-ipaddress':
                # case 'guestinfo.ucm-pub-hostname':
                # case 'guestinfo.ucm-pub-ipaddress':
            case _:
                # v = config.info.value
                # v = config.info.defaultValue
                v = ''

        # propSpec = vim.vApp.PropertySpec()
        propSpec = config
        propSpec.operation = 'edit'
        # propSpec.info = config.info
        propSpec.info.value = v


        new_configSpec.property.append(propSpec)
        # config.info.value = '10.0.1.200'
        # config.info.defaultValue = config.info.defaultValue
    return new_configSpec

def set_vapp_properties():
    # p = ovf_manager.ParseDescriptor(app_ova.get_descriptor(), vim.OvfManager.ParseDescriptorParams(locale='en-US'))


    properties = []
    for p in parse_result.property:
        # print(p.id)

        match p.id:
            case 'guestinfo.Deployment':
                v = 'S'
            case 'guestinfo.isCUCMPub':
                v = 'True'
            case 'guestinfo.remote_enabled':
                v = 'False'
            case 'guestinfo.os_admin':
                v = 'osadmin'
            case 'guestinfo.os_password':
                v = 'l4bp$$D'
            case 'guestinfo.security_password':
                v = 'l4bp$$D'
            case 'guestinfo.appln_user':
                v = 'appadmin'
            case 'guestinfo.appln_pass':
                v = 'l4bp$$D'
            case 'guestinfo.cert_org':
                v = 'AZS'
            case 'guestinfo.cert_unit':
                v = 'IT'
            case 'guestinfo.cert_loc':
                v = 'Chicago'
            case 'guestinfo.cert_state':
                v = 'Illinois'
            case 'guestinfo.cert_country':
                v = 'United States'
            # case 'guestinfo.remote_server_ip':
            # case 'guestinfo.remote_export_dir':
            # case 'guestinfo.remote_login_name':
            # case 'guestinfo.remote_login_password':
            case 'guestinfo.dynamic_cluster_config':
                v = 'True'
            case 'guestinfo.cluster_config_timer':
                v = '3'
            case 'guestinfo.smtp_config':
                v = 'False'
            # case 'guestinfo.smtp':
            # case 'guestinfo.mtu':
            case 'guestinfo.DHCP_Enabled':
                v = 'False'
            case 'guestinfo.hostname':
                v = 'c2-cucm1'
            case 'guestinfo.ipaddress':
                v = '10.0.1.100'
            case 'guestinfo.netmask':
                v = '255.255.255.0'
            case 'guestinfo.Gateway':
                v = '10.0.1.100'
            case 'guestinfo.dns_enabled':
                v = 'True'
            case 'guestinfo.primary_dns':
                v = '10.0.1.20'
            # case 'guestinfo.secondary_dns':
            case 'guestinfo.domain':
                v = 'adanzuniga.com'
            case 'guestinfo.TimeZone':
                v = 'America/Chicago'
            case 'guestinfo.ntp1':
                v = '10.0.1.20'
            # case 'guestinfo.ntp2':
            # case 'guestinfo.ntp3':
            # case 'guestinfo.ntp4':
            # case 'guestinfo.ntp5':
            case 'guestinfo.ucm-sub1-hostname':
                v = 'c2-cucm2'
            case 'guestinfo.ucm-sub1-ipaddress':
                v = '10.0.1.101'
            # case 'guestinfo.ucm-sub2-hostname':
            # case 'guestinfo.ucm-sub2-ipaddress':
            # case 'guestinfo.ucm-sub3-hostname':
            # case 'guestinfo.ucm-sub3-ipaddress':
            # case 'guestinfo.ucm-sub4-hostname':
            # case 'guestinfo.ucm-sub4-ipaddress':
            # case 'guestinfo.ucm-sub5-hostname':
            # case 'guestinfo.ucm-sub5-ipaddress':
            case 'guestinfo.imp-domain':
                v = 'adanzuniga.com'
            case 'guestinfo.imp-sub1-hostname':
                v = 'c2-imp'
            case 'guestinfo.imp-sub1-ipaddress':
                v = '10.0.1.102'
            # case 'guestinfo.imp-sub2-hostname':
            # case 'guestinfo.imp-sub2-ipaddress':
            # case 'guestinfo.imp-sub3-hostname':
            # case 'guestinfo.imp-sub3-ipaddress':
            # case 'guestinfo.imp-sub4-hostname':
            # case 'guestinfo.imp-sub4-ipaddress':
            # case 'guestinfo.imp-sub5-hostname':
            # case 'guestinfo.imp-sub5-ipaddress':
            # case 'guestinfo.ucm-pub-hostname':
            # case 'guestinfo.ucm-pub-ipaddress':
            case _:
                continue

        # property_mapping = vim.vApp.PropertySpec()
        # property_mapping.operation = "add"
        # property_mapping.info = vim.vApp.PropertyInfo()
        # property_mapping.info.key = p.key
        # property_mapping.info.id = p.id
        # property_mapping.info.value = v
        # properties.append(property_mapping)


        properties.append(vim.KeyValue(key=f'.{p.id}.', value=v))

    return properties


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
            deploymentOption='S',
            locale='en-US')
    )
    # print(parse_result)
    # print('\n\n')
    # print('#' * 500)

    updated_v_app_prop = set_vapp_properties()

    cisp = vim.OvfManager.CreateImportSpecParams(
        diskProvisioning=args.disk_provision,  # diskProvisioning (thin/thick/sparse/etc)
        entityName=args.vm_name,
        # hostSystem='',
        # instantiationOst='',
        # ipAllocationPolicy='',
        # ipProtocol='',
        networkMapping=[vim.OvfManager.NetworkMapping(name=interface, network=network)],
        deploymentOption=args.deployment,
        propertyMapping=updated_v_app_prop,
    )

    cisr = ovf_manager.CreateImportSpec(
        ovfDescriptor=ova_xml_descriptor,
        resourcePool=rp,
        datastore=data_store,
        cisp=cisp
    )

    cisr.importSpec.configSpec.cpuAllocation.reservation = 0
    vm_import_spec = cisr.importSpec
    vm_config_spec = vm_import_spec.configSpec
    vap_config = vm_config_spec.vAppConfig

    ncs = generate_new_configSpec()

    # new_configSpec = vim.vApp.VmConfigSpec()
    cisr.importSpec.configSpec.vAppConfig = ncs
    deploy_to_vmware(cisr, rp, dc, app_ova, args)