import re
import textwrap

path = r'C:\Windows\system32\WindowsPowerShell\v1.0\powershell.exe -Command'


def my_f():
    ad_configuration = r"""
    {$securePassword = ConvertTo-SecureString "C0c0a123!" -AsPlainText -Force;

    Import-Module ADDSDeployment;

    Install-ADDSForest
    CreateDnsDelegation:$false
    -DatabasePath "C:\Windows\NTDS"
    -DomainMode "WinThreshold"
    -DomainName "podx.ucalpha.com"
    -DomainNetbiosName "PODX"
    -ForestMode "WinThreshold"
    -InstallDns:$true
    -LogPath "C:\Windows\NTDS"
    -NoRebootOnCompletion:$true
    -SysvolPath "C:\Wi7ndows\SYSVOL"
    -Force:$true
    -SafeModeAdministratorPassword $securePassword;

    Restart-Service -Name DNS;
    Restart-Service -Name NTDS;

    Add-DnsServerPrimaryZone -NetworkId "10.89.242.0/24" -ReplicationScope "Forest"}
    """.strip().replace('\n', ' ')

    ad_configuration = re.sub(r'\s{2,}', ' ', ad_configuration)

    print(f'{path} "& {ad_configuration}')


def myg():
    my_g = textwrap.dedent(r"""
    {Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools;
    $securePassword = ConvertTo-SecureString "C0c0a123!" -AsPlainText -Force;
    Import-Module ADDSDeployment;
    Install-ADDSForest
    -CreateDnsDelegation:$false
    -DatabasePath "C:\Windows\NTDS"
    -DomainMode "WinThreshold"
    -DomainName "podx.ucalpha.com"
    -DomainNetbiosName "PODX"
    -ForestMode "WinThreshold"
    -InstallDns:$true
    -LogPath "C:\Windows\NTDS"
    -NoRebootOnCompletion:$true
    -SysvolPath "C:\Windows\SYSVOL"
    -Force:$true
    -SafeModeAdministratorPassword $securePassword;

    Restart-Service -Name DNS;
    Restart-Service -Name NTDS;

    Add-DnsServerPrimaryZone -NetworkId "10.89.242.0/24" -ReplicationScope "Forest"}
    """).strip()

    my_g = my_g.replace('\n', ' ')

    final = f'{path} "& {my_g}"'

    print(final)


myg()
