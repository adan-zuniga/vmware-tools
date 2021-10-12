def get_dc(args, si):
    """
    Get a datacenter by its name.
    """
    if dc_name := args.datacenter_name:
        for datacenter in si.content.rootFolder.childEntity:
            if datacenter.name == dc_name:
                return datacenter
        raise Exception('Failed to find datacenter named %s' % dc_name)
    else:
        return si.content.rootFolder.childEntity[0]



