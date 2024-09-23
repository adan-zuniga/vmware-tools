from pyVmomi import vim, vmodl
import time

def get_vm_by_name(service_instance, vm_name):


    content = service_instance.RetrieveContent()
    folder = content.rootFolder  # starting point to look into
    view_type = [vim.VirtualMachine]  # object types to look for
    recursive = True  # whether we should look into it recursively
    container = content.viewManager.CreateContainerView(folder, view_type, recursive)

    for managed_object_ref in container.view:
        if managed_object_ref.name == vm_name:
            vm_obj = managed_object_ref
            return vm_obj
    return None

def deploy_to_vmware(cisr, rp: vim.ResourcePool, dc: vim.Datacenter, ova_handle, esxi):


    if cisr.error:
        print("The following errors will prevent import of this OVA:")
        for error in cisr.error:
            print(f'{error}')
            exit()
    else:

        ova_handle.set_spec(cisr)
        lease = rp.ImportVApp(spec=cisr.importSpec, folder=dc.vmFolder)

        while lease.state == vim.HttpNfcLease.State.initializing:
            print('Waiting for lease to be ready...')
            time.sleep(1)

        if lease.state == vim.HttpNfcLease.State.error:
            print(f'Lease error: {lease.error}')
            return 1
        if lease.state == vim.HttpNfcLease.State.done:
            return 0

        print('Starting deploy...')

        ova_handle.upload_disks(lease, esxi.host)

        return True