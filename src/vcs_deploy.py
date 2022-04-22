from pyVmomi import vim, vmodl


config = vm.config
configSpec = vim.vApp.VmConfigSpec()
for prop in config.vAppConfig.property:
    # logger.info(f'property: {prop.id}')
    """
    We only worry about the following:
    system.hostname
    default.dns - only on EE
    ipv4.address
    ipv4.netmask
    ipv4.gateway
    ntp.servers - use our internals
    ssh.public.key

    Not modified:
    domain.name - this might be different from inside.
    ip4.enable
    ip6.enable
    ip6.address
    ip6.gateway
    ssh.enabled
    webui.enabled
    system.timezone
    """
    if prop.id == "system.hostname":
        propSpec = vim.vApp.PropertySpec()
        propSpec.operation = 'edit'
        propSpec.info = prop
        propSpec.info.value = server.hostname
        # logger.info(f' Setting {prop.id} to {propSpec.info.value}')
        configSpec.property.append(propSpec)

    if prop.id == "default.dns":
        propSpec = vim.vApp.PropertySpec()
        propSpec.operation = 'edit'
        propSpec.info = prop

        if server.is_expressway_core:
            dns = ",".join(
                [x.data for x in server.deployment.options.filter(name__startswith='dns', name__endswith='ip')])
            propSpec.info.value = dns
            # logger.info(f' Setting {prop.id} to {propSpec.info.value}')
            configSpec.property.append(propSpec)

        if server.is_expressway_edge:
            propSpec.info.value = "64.73.0.21, 64.73.0.53, 64.73.128.21, 64.73.128.53"
            # logger.info(f' Setting {prop.id} to {propSpec.info.value}')
            configSpec.property.append(propSpec)

    if prop.id == "ip4.address":
        propSpec = vim.vApp.PropertySpec()
        propSpec.operation = 'edit'
        propSpec.info = prop
        propSpec.info.value = server.ip
        # logger.info(f' Setting {prop.id} to {propSpec.info.value}')
        configSpec.property.append(propSpec)

    if prop.id == "ip4.netmask":
        propSpec = vim.vApp.PropertySpec()
        propSpec.operation = 'edit'
        propSpec.info = prop
        propSpec.info.value = str(server.mask)
        # logger.info(f' Setting {prop.id} to {propSpec.info.value}')
        configSpec.property.append(propSpec)

    if prop.id == "ip4.gateway":
        propSpec = vim.vApp.PropertySpec()
        propSpec.operation = 'edit'
        propSpec.info = prop
        propSpec.info.value = str(server.network.gateway)
        # logger.info(f' Setting {prop.id} to {propSpec.info.value}')
        configSpec.property.append(propSpec)

    if prop.id == "ntp.servers":
        propSpec = vim.vApp.PropertySpec()
        propSpec.operation = 'edit'
        propSpec.info = prop
        propSpec.info.value = "64.73.0.24, 64.73.0.56, 64.73.128.24, 64.73.128.56"
        # logger.info(f' Setting {prop.id} to {propSpec.info.value}')
        configSpec.property.append(propSpec)

    # Move this from static to variable - this is in staging.pub
    if prop.id == "ssh.public.key":
        propSpec = vim.vApp.PropertySpec()
        propSpec.operation = 'edit'
        propSpec.info = prop
        propSpec.info.value = "ssh-rsa yourkeyhere@h-hcsutildev-ord-1"
        # logger.info(f' Setting {prop.id} to {propSpec.info.value}')
        configSpec.property.append(propSpec)


cspec.vAppConfig = configSpec

# logger.info(f'  Reconfiguring {server.hostname} general settings')
reconfigure_vm(cluster, server.hostname, cspec)