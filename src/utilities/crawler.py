from pyVmomi import vim


def get_dc(args, si):
    """
    Get a datacenter by its name.
    """
    if dc_name := args.datacenter_name:
        for datacenter in si.content.rootFolder.childEntity:
            if datacenter.name == dc_name:
                return datacenter
        raise Exception(f'Failed to find datacenter named {dc_name}')
    else:
        return si.content.rootFolder.childEntity[0]


def get_resource_pool(args, si, datacenter):
    if args.resource_pool:
        """
        Get a resource pool in the datacenter by its names.
        """

        view_manager = si.content.viewManager
        container_view = view_manager.CreateContainerView(datacenter, [vim.ResourcePool], True)
        try:
            for resource_pool in container_view.view:
                if resource_pool.name == args.resource_pool:
                    return resource_pool
        finally:
            container_view.Destroy()
        raise Exception(f'Failed to find resource pool {args.resource_pool} in datacenter {datacenter.name}')

    else:
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
            raise Exception(f'Failed to find a resource pool in datacenter {datacenter.name}')
        return largest_rp


def get_data_store(args, datacenter):
    if args.datastore_name:
        """
        Pick a datastore by its name.
        """
        for datastore in datacenter.datastore:
            try:
                if datastore.name == args.datastore_name:
                    return datastore
            except Exception:  # Ignore datastores that have issues
                pass
        raise Exception(f'Failed to find {args.datastore_name} on datacenter {datacenter.name}')
        # datastore = get_ds(datacenter, args.datastore_name)
    else:
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
            raise Exception(f'Failed to find any free datastores on {datacenter.name}')
        return largest
        # datastore = get_largest_free_ds(datacenter)


def get_net_mappings(args, datacenter):
    if args.network:
        for network in datacenter.network:
            if network.name == args.network:
                return network
        raise Exception(f'Failed to find network named {args.network}')
    else:
        raise Exception(f'Failed to find network named {args.network}')