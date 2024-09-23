import atexit
from datetime import datetime
import logging
from ipaddress import ip_address
import os
import re
import sys
from time import sleep
from xml.dom.minidom import parseString

# https://stackoverflow.com/questions/20801976/run-powershell-command-with-pipeline-in-cmd


def add_file_logger(cfg_log_level='INFO', home_directory=''):
    """Configure script logging."""
    log_fmt = logging.Formatter(
        fmt='{asctime}.{msecs:0<3.0f} [{module:^13}] [{levelname:^10}]: {message}',
        datefmt='%Y-%m-%d %H:%M:%S',
        style='{')
    level = cfg_log_level

    file_log = logging.FileHandler(os.path.join(home_directory, 'ovfset.log'))
    file_log.setLevel(level)
    file_log.setFormatter(log_fmt)
    # file_log.addFilter(file_fmt_filter)
    logging.getLogger().addHandler(file_log)

    console_log = logging.StreamHandler()
    console_log.setLevel(level)
    console_log.setFormatter(log_fmt)
    logging.getLogger().addHandler(console_log)


def log_end_of_script():
    """Log script end regardless of how script is terminated."""
    # for l in logger.handlers:
    #     l.removeFilter(file_fmt_filter)
    logger.info('OVF Configurator Script Ends.\n' + '\n' * 2)


def file_fmt_filter(record):
    # record.msg = os.linesep.join([s for s in record.msg.splitlines() if s])
    record.msg = record.msg
    return True


class NetDetails:
    """
    A class to represent network details to use to configure the system.

    Attributes:
        if_name (str): Interface name to apply network settings to.
        connection_uuid (str): Connection UUID (Only applicable to Linux).
        ip (str): IP address for the system.
        sm (str): Subnet mask for the system.
        gw (str): Default gateway for the system.
        hostname (str): Hostname for the system.
        dns (str): DNS servers for the system.
    """

    def __init__(self, ip, sm, dg, hostname, dns):
        """
        Constructs all the necessary attributes for the NetDetails object.

        Args:
            ip (str): IP address for the system.
            sm (str): Subnet mask for the system.
            dg (str): Default gateway for the system.
            hostname (str): Hostname for the system.
            dns (str): DNS servers for the system.
        """
        self.if_name = ''
        self.connection_uuid = ''

        self.ip = self._is_valid_ip(ip, 'IP Address')
        self.sm = self._check_subnet_mask(sm)
        self.gw = self._is_valid_ip(dg, 'Default Gateway')

        self.hostname = hostname

        self.dns = self._check_dns_servers(dns)

    def _check_dns_servers(self, dns):
        """
        Validate and return the DNS servers to configure on the system.

        Args:
            dns (str): Comma-separated DNS servers.

        Returns:
            str: Validated primary and secondary DNS servers(joinned by comma, if two servers are provided).
        """
        dns_servers = dns.split(',')

        primary_dns = dns_servers[0].strip()
        secondary_dns = ''

        primary_dns = self._is_valid_ip(primary_dns, 'DNS Server')

        try:
            secondary_dns = dns_servers[1].strip()
        except IndexError:
            pass
        else:
            secondary_dns = self._is_valid_ip(secondary_dns, 'DNS Server')
        finally:
            return ','.join([d for d in [primary_dns, secondary_dns] if d])

    def _check_subnet_mask(self, sm):
        """
        Validate and return the subnet mask.

        Args:
            sm (str): Subnet mask for the system.

        Returns:
            str: Validated subnet mask.
        """
        try:
            subnet_mask_int = int(sm)
        except ValueError:
            logger.error(f'{sm} is not a valid Subnet Mask.')
            exit()
        else:
            if 0 <= subnet_mask_int <= 32:
                return sm
            else:
                logger.error(f'{sm} is not a valid Subnet Mask.')
                exit()

    def _is_valid_ip(self, ip, usage):
        """
        Validate and return an IP address.

        Args:
            ip (str): IP address to be validated.
            usage (str): Usage of the IP address to be validated.

        Returns:
            str: Validated IP address.
        """
        try:
            ip_address(ip)
            return ip
        except ValueError:
            logger.error(f'{ip} is not a valid {usage}.')
            exit()


def execute_system_command(log_prefix='', log_suffix='', strip_cmd_result=True):
    """
    Decorator to execute a command, log its execution, and optionally strip the result.

    Args:
        log_prefix (str): Prefix to add to the log message.
        log_suffix (str): Suffix to add to the log message.
        strip_cmd_result (bool): Whether to strip the command result of leading/trailing whitespace.

    Returns:
        function: The wrapped function that executes the command and logs the result.
    """
    def decorator(func):
        def wrapper(self):
            """
            Wrapper function to execute the command and log the result.

            Args:
                self: The instance of the class containing the command.

            Returns:
                str: The result of the executed command.
            """
            a_formatted_command = func(self)

            logger.info(f'Executing: {a_formatted_command}')
            command_result = os.popen(a_formatted_command).read()

            if strip_cmd_result:
                command_result = command_result.strip()

            logger.info(f'{log_prefix}{command_result}{log_suffix}')

            return command_result

        return wrapper

    return decorator


def extract_property(formatted_xml, prop_search_string, suffix=''):
    """
    Extracts the value of a property from a formatted vApp XML string.

    Args:
        formatted_xml (str): The vApp XML string to search within.
        prop_search_string (str): The property name to search for.
        suffix (str): A suffix to append to the log message.

    Returns:
        str: The value of the property if found, otherwise an empty string.
    """
    prop_value = re.findall(rf'.*{prop_search_string}.*="(.*)".*', string=formatted_xml)
    if prop_value:
        prop_value = prop_value[0]
    else:
        prop_value = ''

    logger.info(f'{prop_search_string:.<15} {prop_value}{suffix}')
    return prop_value


class PlatformDetails:
    """
    A class to handle platform-specific details and operations.

    Attributes:
        platform (str): The platform type (e.g., 'linux', 'win32').
        nd (NetDetails): An instance of NetDetails containing network configuration for the system.
        state_file (str): Path to the state file.
        vmtools_path (str): Path to the VMware tools executable.
        ps_path (str): Path to the PowerShell executable.
    """
    def __init__(self):
        """
        Initializes the PlatformDetails class with platform-specific settings.
        """
        self.platform = sys.platform.lower()
        self.nd = None
        if self.platform in ['linux']:
            self.home_dir = r'/opt/ovfset'
            self.vmtools_path = 'vmtoolsd'
            self.ps_path = ""
        elif self.platform == 'win32':
            self.home_dir = r'C:\Program Files\ovfset'
            self.vmtools_path = r'"C:\Program Files\VMware\VMware Tools\vmtoolsd.exe"'
            self.ps_path = r'C:\Windows\system32\WindowsPowerShell\v1.0\powershell.exe -Command'

        self.state_file = os.path.join(self.home_dir, 'state.txt')

    def check_if_state_file_exists(self):
        """Exit execution if state file exists due to previous successful system configuration."""
        if os.path.exists(self.state_file):
            logging.info(f'Delete {self.state_file}  and reboot to configure system from vApp properties.')
            exit()

    @execute_system_command(log_prefix='Set Hostname Result:\n')
    def set_system_hostname(self):
        """
        Set the system hostname.

        Returns:
            str: The platform-specific command to set the hostname.
        """
        d = dict(
            linux=f'hostnamectl set-hostname {self.nd.hostname} --static',
            win32=f'{self.ps_path} "Rename-Computer -NewName {self.nd.hostname}"'
        )
        return d[self.platform]

    @execute_system_command(log_prefix='Set IP Result:\n', log_suffix='\n')
    def set_system_ip(self):
        """
        Set the system IP address.

        Returns:
            str: The platform-specific command to set the IP address.
        """
        self.nd.if_name = self.get_interface_name()

        d = dict(
            linux=f'nmcli connection add con-name "{self.nd.if_name}" ifname {self.nd.if_name} type ethernet ip4 {self.nd.ip}/{self.nd.sm} gw4 {self.nd.gw}',
            win32=f'{self.ps_path} "New-NetIPAddress –InterfaceAlias {self.nd.if_name} –IPAddress {self.nd.ip} –PrefixLength {self.nd.sm} -DefaultGateway {self.nd.gw}"',
        )

        if self.platform == 'linux':
            self.nd.connection_uuid = self.get_connection_uuid()
            self.delete_connection()

        return d[self.platform]

    @execute_system_command(log_prefix='Set DNS Result:\n')
    def set_system_dns(self):
        """
        Set the system DNS servers.

        Returns:
            str: The platform-specific command to set the DNS servers.
        """
        # dns = ','.join(filter(None, [self.nd.primary_dns, self.nd.secondary_dns]))

        d = dict(
            linux=f'nmcli connection modify "{self.nd.if_name}" ipv4.dns "{self.nd.if_name}"',
            win32=f'{self.ps_path} "Set-DnsClientServerAddress -InterfaceAlias {self.nd.if_name} -ServerAddresses {self.nd.dns}"'
        )
        return d[self.platform]

    @execute_system_command(log_prefix='Found Interface: ')
    def get_interface_name(self):
        """
        Get the network interface name.

        Returns:
            str: The platform-specific command to get the interface name.
        """

        d = dict(
            linux="nmcli device | grep ethernet | awk '{print $1}'",
            win32=f'{self.ps_path} "& {{Get-NetAdapter | Select -expand Name}}"'
        )
        return d[self.platform]

    @execute_system_command(log_prefix='\n' * 2, strip_cmd_result=False)
    def extract_v_app_properties(self):
        """
        Extract vApp properties using VMware tools.

        Returns:
            str: The platform-specific command to extract vApp properties.
        """
        cmd = f'{self.vmtools_path} --cmd "info-get guestinfo.ovfEnv"'
        return cmd

    def process_v_app_properties(self, ovf_env_string):
        """
        Processes the vApp properties from the OVF environment string.

        Args:
            ovf_env_string (str): The OVF environment string.

        Returns:
            NetDetails: An instance of NetDetails with the extracted properties.
        """
        if not ovf_env_string or ovf_env_string.lower() in ['no value found']:
            logger.error('vApp Options were not injected correctly.')
            exit()

        ovf_env_dom = parseString(ovf_env_string)
        pxml = ovf_env_dom.toprettyxml()

        logger.info(f'{"Extracted Properties:":_^100}')

        ip_add = extract_property(pxml, 'IP')
        subnet_mask = extract_property(pxml, 'Netmask')
        gateway = extract_property(pxml, 'DefaultGateway')
        hostname = extract_property(pxml, 'Hostname')
        dns = extract_property(pxml, 'DNS', '\n')

        if not all([ip_add, subnet_mask, gateway]):
            logging.error(f'Missing network details.')
            exit()

        nd = NetDetails(ip=ip_add, sm=subnet_mask, dg=gateway, hostname=hostname, dns=dns)

        logging.info(f'{vars(nd)}')
        self.nd = nd
        return nd

    @execute_system_command(log_prefix='Found Connection UUID: ')
    def get_connection_uuid(self):
        """
        Get the connection UUID for the network interface on Linux.

        Returns:
            str: The Linux command to get the connection UUID.
        """
        return "nmcli connection show | grep ethernet | awk '{print $(NF-2)}'"

    @execute_system_command()
    def delete_connection(self):
        """
        Deletes the network connection using the connection UUID on Linux.

        Returns:
            str: The Linux command to delete the network connection.
        """
        return f'nmcli connection delete uuid {self.nd.connection_uuid}'

    @execute_system_command()
    def reboot(self):
        """
        Reboot the system after 3 seconds

        Returns:
            str: The platform-specific command to restart the system.
        """
        sleep(3)
        d = dict(
            linux="reboot",
            win32=f'{self.ps_path} "Restart-Computer"'
        )
        return d[self.platform]

    def write_state_file(self):
        with open(self.state_file, mode='a') as state_file:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            msg = f'System successfully configured on: {now}\n'
            state_file.write(msg)


if __name__ == '__main__':

    atexit.register(log_end_of_script)

    plat_details = PlatformDetails()

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    add_file_logger(home_directory=plat_details.home_dir)
    logger.info('OVF Configurator Script Starts.')

    plat_details.check_if_state_file_exists()

    ovf_env_str = plat_details.extract_v_app_properties()
    plat_details.process_v_app_properties(ovf_env_str)

    plat_details.set_system_ip()
    plat_details.set_system_dns()
    plat_details.set_system_hostname()
    plat_details.write_state_file()
    plat_details.reboot()
