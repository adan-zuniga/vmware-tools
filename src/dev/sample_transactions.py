from pyVim import connect
from pyVmomi import vim
from src.utilities import get_vm_by_name


def host_details(service_instance):
    """
    Get Details about ESXi
    """
    esxi_version = service_instance.content.about.fullName
    esxi_major_version = service_instance.content.about.version
    print(esxi_major_version)


def find_vm_by_dns(service_instance):
    searcher = service_instance.content.searchIndex
    vms = searcher.FindAllByDnsName(dnsName='adanzuniga.com', vmSearch=True)
    print(vms[0])


def find_vm_by_ip(service_instance):
    content = service_instance.RetrieveContent()
    print(content)
    searcher = service_instance.content.searchIndex

    vm = searcher.FindAllByIp(ip="10.0.1.10", vmSearch=True)
    vm = vm[0]
    print(f"{' VM ':#^170}")
    print(vm.config.name)
    print(*vars(vm.config).items(), sep='\n')

    connect.Disconnect(service_instance)


def get_all_vms(service_instance):
    """
    LINKS

    `PyVmomi Repository <https://github.com/vmware/pyvmomi>`_
    `Vsphere API Tutorial
    <https://www.jacobtomlinson.co.uk/posts/2016/getting-started-with-vmwares-esxi/vsphere-api-in-python/>`_
    `Vsphere API Tutorial 2
    <https://www.vcloudnine.de/first-steps-with-python-and-pyvmomi-vsphere-sdk-for-python/?cn-reloaded=1>`_
    `PyVmomi Documentation <https://www.vmware.com/support/orchestrator/doc/vro-vsphere65-api/left-pane.html>`_
    """

    # print(*vars(service_instance.content).items(), sep='\n')
    # search_methods = service_instance.content.searchIndex
    content = service_instance.RetrieveContent()

    container = content.rootFolder  # starting point to look into
    view_type = [vim.VirtualMachine]  # object types to look for
    recursive = True  # whether we should look into it recursively
    container_view = content.viewManager.CreateContainerView(
        container, view_type, recursive)

    children = container_view.view
    for child in children:
        print(f'VM ------- {child.name}')
        networks = child.network
        if len(networks) == 1:  # How Many Networks
            print(networks[0].name)
        else:
            network_list = [net.name for net in networks]
            print(f'{"Networks: " + str(network_list):^60}')
        data_stores = child.datastore
        if len(data_stores) == 1:
            print(data_stores[0].name)
        else:
            dss = [ds for ds in data_stores]
            print(dss)


def get_dir(o):
    for d in dir(o):
        if not d.startswith('__'):
            print(f'{d:_<50}', getattr(o, d))


def get_licence(service_instance):
    licenses = service_instance.content.licenseManager.licenses
    for esxi_license in licenses:
        print(esxi_license.licenseKey)
        print(esxi_license.name)


def methods(service_instance):
    # get_dir(service_instance.content)
    elements = service_instance.content
    get_dir(elements)

    # for element in elements:
    #     get_dir(element)
    #     print(element.licenseKey)
    #     print(element.name)
    # get_dir(service_instance.content.about) # Host info
    # get_dir(service_instance.viewManager)
    exit()


def shutdown_cucm(service_instance):
    # entity_stack = service_instance.content.rootFolder.childEntity
    content = service_instance.RetrieveContent()
    container = content.rootFolder
    container_view = content.viewManager.CreateContainerView(
        container=container, type=[], recursive=True
    )
    for entity in container_view.view:
        if entity.name == 'Fedora':
            # entity.PowerOn()
            # get_dir(entity.config.hardware.device)
            devices = entity.config.hardware.device
            for d in devices:
                desc = d.deviceInfo.label
                if 'Network' in desc:
                    spec = vim.vm.device.VirtualDeviceSpec()
                    print(spec)
                    print()
                    # print(desc)
                    # print(d.macAddress)
                    # print(d.connectable.connected)
                    # d.connectable.connected = False
                    # d.connectable.startConnected = False

            # for net in entity.network:
            #     get_dir(net)




if __name__ == '__main__':
    esxi_instance = connect.SmartConnectNoSSL(
        host='172.18.9.5',
        user='root',
        pwd='l4bp$$D',
        port=443
    )
    # shutdown_cucm(esxi_instance)
    # print()
    my_vm_obj = get_vm_by_name(esxi_instance, 'C2-IMP')
    print(my_vm_obj)

    cspec = vim.vm.ConfigSpec()
    config = my_vm_obj.config
    configSpec = vim.vApp.VmConfigSpec()
    for prop in config.vAppConfig.property:
        print(prop.info.id)
