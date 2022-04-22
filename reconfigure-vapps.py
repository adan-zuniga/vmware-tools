#!/usr/bin/env python
"""
Written by Dann Bohn
Github: https://github.com/whereismyjetpack
Email: dannbohn@gmail.com

Script to add a Hard disk to an existing VM
This is for demonstration purposes only.
I did not do a whole lot of sanity checking, etc.

Known issues:
This will not add more than 15 disks to a VM
To do that the VM needs an additional scsi controller
and I have not yet worked through that
"""
from pyVmomi import vim
from pyVim.task import WaitForTask
from samples.tools import pchelper, service_instance
from utilities.home_esxi import ESXi


def return_conf_spec():
    spec = vim.vm.ConfigSpec()
    spec.vAppConfig = vim.vApp.VmConfigSpec()
    return spec


def main(reconfig=False):
    """
    Sample for adding a disk to vm
    """

    vm = None
    if args.uuid:
        search_index = si.content.searchIndex
        vm = search_index.FindByUuid(None, args.uuid, True)
    elif args.vm_name:
        content = si.RetrieveContent()
        vm = pchelper.get_obj(content, [vim.VirtualMachine], args.vm_name)

    if vm:
        print(vm.config)
        if reconfig:
            spec = return_conf_spec()
            WaitForTask(vm.ReconfigVM_Task(spec=spec))
    else:
        print("VM not found")


# start this thing
if __name__ == "__main__":
    args = ESXi()
    si = service_instance.connect(args)
    main(reconfig=False)