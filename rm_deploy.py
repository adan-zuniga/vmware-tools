def deploy_ova(cluster, hostname, ova, deploymentoption, vlan, folder, datastore=None, filters=None):

    vcenter = cluster.datacenter.vcenter

    # Retrieve credentials for this vcenter
    creds = get_credentials(f'mca/vcenter/{vcenter.hostname}')
    if not creds:
        raise Exception(f'Could not retrieve credentials for {vcenter.hostname}')

    try:
        service_instance = None
        sslContext = None

        if not vcenter.verifySSL:
            sslContext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            sslContext.verify_mode = ssl.CERT_NONE

            # disable urllib3 warnings
            if hasattr(requests.packages.urllib3, 'disable_warnings'):
                requests.packages.urllib3.disable_warnings()

        try:
            service_instance = connect.SmartConnect(host=vcenter.ip,
                                                    user=creds['username'],
                                                    pwd=creds['password'],
                                                    port=int(vcenter.port),
                                                    sslContext=sslContext)
        except IOError as e:
            pass

        if not service_instance:
            raise Exception(f'Could not connect to {vcenter.hostname} on port {vcenter.port} using specified username and password')

        content = service_instance.RetrieveContent()
        session_manager = content.sessionManager

        """
        Verify our datacenter is ok
        """
        dc_obj = get_obj(content, [vim.Datacenter], cluster.datacenter.name)
        if not dc_obj:
            raise SystemExit()

        cluster_obj = get_obj(content, [vim.ClusterComputeResource], cluster.name)
        if not cluster_obj:
            raise Exception(f' cluster_obj is {cluster_obj}')


        """
        Get the Resource Pool
        """
        resource_pool = get_resource_pool(content, cluster_obj)

        datastore = get_largest_free_ds(cluster_obj, filters)

        ova_handle = OvaHandler(ova.file.path)
        ovfManager = content.ovfManager

        # Load the OvaInfo for this OVA.
        ova_info = OvaInfo(ova_handle.get_descriptor())
        # Get the network interfaces
        xdn = ova_info.get('NetworkSection', 'Network')
        if not isinstance(xdn, list):
            xdn = [xdn]

        # We only ever worry about the first one - even on our Expressways as we do
        # Expressway on a stick with a public IP on the Edge.
        ova_network = xdn[0]['@ovf:name']

        # CreateImportSpecParams can specify many useful things such as
        # diskProvisioning (thin/thick/sparse/etc)
        # networkMapping (to map to networks)
        # propertyMapping (descriptor specific properties)
        cisp = vim.OvfManager.CreateImportSpecParams()
        cisp.deploymentOption = str(deploymentoption)
        cisp.entityName = hostname
        cisp.diskProvisioning = 'thick'

        network = get_obj(content, [vim.Network], vlan.name)
        # Virtual interface is the name of the port group network
        nma = vim.OvfManager.NetworkMapping.Array()
        # Let the name equal to VM Network and not the name of the portgroup network
        nm = vim.OvfManager.NetworkMapping(name=ova_network, network=network)
        nma.append(nm)
        cisp.networkMapping = nma

        cisr = ovfManager.CreateImportSpec(ova_handle.get_descriptor(),
                                           resource_pool, datastore, cisp)

        # These errors might be handleable by supporting the parameters in
        # CreateImportSpecParams
        if len(cisr.error):
            for error in cisr.error:
            raise Exception(cisr.error)

        ova_handle.set_spec(cisr)

        lease = resource_pool.ImportVApp(cisr.importSpec, dc_obj.vmFolder)
        while lease.state == vim.HttpNfcLease.State.initializing:
            time.sleep(1)

        if lease.state == vim.HttpNfcLease.State.error:
            if lease.error == vim.fault.DuplicateName:
                return 0
            else:
                return 1

        if lease.state == vim.HttpNfcLease.State.done:
            return 0

        ova_handle.upload_disks(lease, vcenter.ip, vcenter.port)

        vm = get_obj(content, [vim.VirtualMachine], hostname)
        if not vm:
            return 1

        vmfolder = get_obj(content, [vim.Folder], folder)
        if not vmfolder:

            parent = get_obj(content, [vim.Folder], 'Customers')
            parent.CreateFolder(folder)
            vmfolder = get_obj(content, [vim.Folder], folder)

        if vmfolder:
            task = vmfolder.MoveIntoFolder_Task([vm])
            tasks.wait_for_tasks(service_instance, [task])
        else:

    except vmodl.MethodFault as e:
        connect.Disconnect(service_instance)
        raise Exception(f'Caught vmodl fault: {e.msg}')

    connect.Disconnect(service_instance)