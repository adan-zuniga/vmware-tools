import os
import re
import sys
from textwrap import dedent

my_string = """

"""


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

            print(f'Executing: {a_formatted_command}')
            command_result = os.popen(a_formatted_command).read()

            if strip_cmd_result:
                command_result = command_result.strip()

            print(f'{log_prefix}{command_result}{log_suffix}')

            return command_result

        return wrapper

    return decorator


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

    @execute_system_command(log_prefix='')
    def get_interface_name(self):
        """
        Get the network interface name.

        Returns:
            str: The platform-specific command to get the interface name.
        """

        ad_configuration = dedent(r"""
        Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools;

        $securePassword = ConvertTo-SecureString "C0c0a123!" -AsPlainText -Force;

        Import-Module ADDSDeployment;

        Install-ADDSForest
        -CreateDnsDelegation:$false
        -DatabasePath "C:\Windows\NTDS"
        -DomainMode "WinThreshold"
        -DomainName "podx.ucalpha.com"
        -DomainNetbiosName "PODX"
        -ForestMode "WinThreshold"
        -InstallDns:$false
        -LogPath "C:\Windows\NTDS"
        -NoRebootOnCompletion:$true
        -SysvolPath "C:\Windows\SYSVOL"
        -Force:$true
        -SafeModeAdministratorPassword $securePassword;

        Restart-Service -Name DNS;
        Restart-Service -Name NTDS;

        Add-DnsServerPrimaryZone -NetworkId "10.89.242.0/24" -ReplicationScope "Forest"
        """).strip()

        ad_configuration = ad_configuration.replace('\n', ' ')

        d = dict(
            linux="N/A",
            # win32=f'{self.ps_path} "& {{get-windowsfeature | Select -expand Name}}"'
            # win32=f'{self.ps_path} "& {{Install-WindowsFeature -Name AD-Domain-Services, GPMC, DNS}}"'
            # win32=f'{self.ps_path} "& {{Install-WindowsFeature -Name AD-Domain-Services, GPMC, DNS, AD-Certificate}}"'
            # win32=f'{self.ps_path} "& {{Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools}}"'
            # win32=f'{self.ps_path} "& {{Uninstall-WindowsFeature -Name AD-Domain-Services, GPMC, DNS, AD-Certificate}}"'
            win32=f'{self.ps_path} "& {ad_configuration}'
        )
        # AD-Certificate
        # AD-Domain-Services
        # DNS
        return d[self.platform]


if __name__ == '__main__':
    plat = PlatformDetails()
    plat.get_interface_name()

