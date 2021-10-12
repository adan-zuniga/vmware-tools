#!/usr/bin/env python
"""
Written by Nathan Prziborowski
Github: https://github.com/prziborowski

This code is released under the terms of the Apache 2
http://www.apache.org/licenses/LICENSE-2.0.html

Deploy an ova file either from a local path or a URL.
Most of the functionality is similar to ovf except that
that an OVA file is a "tarball" so tarfile module is leveraged.

"""
import sys
import time

from utilities.virtualtemplates import OvfHandler

from samples.tools import cli, service_instance

from pyVmomi import vim, vmodl

__author__ = 'azuniga'


def main():
    parser = cli.Parser()
    parser.add_optional_arguments(cli.Argument.OVA_PATH, cli.Argument.DATACENTER_NAME,
                                  cli.Argument.RESOURCE_POOL, cli.Argument.DATASTORE_NAME)
    args = parser.get_args()
    si = service_instance.connect(args)

    if args.datacenter_name:
        datacenter = get_dc(si, args.datacenter_name)
    else:
        datacenter = si.content.rootFolder.childEntity[0]

    if args.resource_pool:
        resource_pool = get_rp(si, datacenter, args.resource_pool)
    else:
        resource_pool = get_largest_free_rp(si, datacenter)

    if args.datastore_name:
        datastore = get_ds(datacenter, args.datastore_name)
    else:
        datastore = get_largest_free_ds(datacenter)

    ovf_handle = OvfHandler(args.ova_path)

    ovf_manager = si.content.ovfManager
    # CreateImportSpecParams can specify many useful things such as
    # diskProvisioning (thin/thick/sparse/etc)
    # networkMapping (to map to networks)
    # propertyMapping (descriptor specific properties)
    cisp = vim.OvfManager.CreateImportSpecParams()
    cisr = ovf_manager.CreateImportSpec(
        ovf_handle.get_descriptor(), resource_pool, datastore, cisp)

    # These errors might be handleable by supporting the parameters in
    # CreateImportSpecParams
    if cisr.error:
        print("The following errors will prevent import of this OVA:")
        for error in cisr.error:
            print("%s" % error)
        return 1

    ovf_handle.set_spec(cisr)

    lease = resource_pool.ImportVApp(cisr.importSpec, datacenter.vmFolder)
    while lease.state == vim.HttpNfcLease.State.initializing:
        print("Waiting for lease to be ready...")
        time.sleep(1)

    if lease.state == vim.HttpNfcLease.State.error:
        print("Lease error: %s" % lease.error)
        return 1
    if lease.state == vim.HttpNfcLease.State.done:
        return 0

    print("Starting deploy...")
    return ovf_handle.upload_disks(lease, args.host)


def get_dc(si, name):
    """
    Get a datacenter by its name.
    """
    for datacenter in si.content.rootFolder.childEntity:
        if datacenter.name == name:
            return datacenter
    raise Exception('Failed to find datacenter named %s' % name)


def get_rp(si, datacenter, name):
    """
    Get a resource pool in the datacenter by its names.
    """
    view_manager = si.content.viewManager
    container_view = view_manager.CreateContainerView(datacenter, [vim.ResourcePool], True)
    try:
        for resource_pool in container_view.view:
            if resource_pool.name == name:
                return resource_pool
    finally:
        container_view.Destroy()
    raise Exception("Failed to find resource pool %s in datacenter %s" %
                    (name, datacenter.name))


def get_largest_free_rp(si, datacenter):
    """
    Get the resource pool with the largest unreserved memory for VMs.
    """
    view_manager = si.content.viewManager
    container_view = view_manager.CreateContainerView(datacenter, [vim.ResourcePool], True)
    largest_rp = None
    unreserved_for_vm = 0
    try:
        for resource_pool in container_view.view:
            if resource_pool.runtime.memory.unreservedForVm > unreserved_for_vm:
                largest_rp = resource_pool
                unreserved_for_vm = resource_pool.runtime.memory.unreservedForVm
    finally:
        container_view.Destroy()
    if largest_rp is None:
        raise Exception("Failed to find a resource pool in datacenter %s" % datacenter.name)
    return largest_rp


def get_ds(datacenter, name):
    """
    Pick a datastore by its name.
    """
    for datastore in datacenter.datastore:
        try:
            if datastore.name == name:
                return datastore
        except Exception:  # Ignore datastores that have issues
            pass
    raise Exception("Failed to find %s on datacenter %s" % (name, datacenter.name))


def get_largest_free_ds(datacenter):
    """
    Pick the datastore that is accessible with the largest free space.
    """
    largest = None
    largest_free = 0
    for datastore in datacenter.datastore:
        try:
            free_space = datastore.summary.freeSpace
            if free_space > largest_free and datastore.summary.accessible:
                largest_free = free_space
                largest = datastore
        except Exception:  # Ignore datastores that have issues
            pass
    if largest is None:
        raise Exception('Failed to find any free datastores on %s' % datacenter.name)
    return largest


if __name__ == "__main__":
    sys.exit(main())