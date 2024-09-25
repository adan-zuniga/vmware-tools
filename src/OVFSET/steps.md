1. ### Install AD-Domain-Services
   2. `Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools`
   `Success Restart Needed Exit Code Feature Result`
   `------- -------------- ---------      --------------`
   `True    No             Success        {Active Directory Domain Services, Group P...`

2. ### Promote to Domain Controller
   4. `$securePassword = ConvertTo-SecureString "C0c0a123!" -AsPlainText -Force`
      5. **No Output**
   5. `Import-Module ADDSDeployment`
   6. `Install-ADDSForest -DatabasePath "C:\Windows\NTDS" -DomainMode "WinThreshold" -DomainName "podx.ucalpha.com" -DomainNetbiosName "PODX" -ForestMode "WinThreshold" -InstallDns:$false -LogPath "C:\Windows\NTDS" -NoRebootOnCompletion:$true -SysvolPath "C:\Windows\SYSVOL" -Force:$true -SafeModeAdministratorPassword $securePassword`
   6. `Install-ADDSForest -DomainMode "WinThreshold" -DomainName "podx.ucalpha.com" -ForestMode "WinThreshold" -NoRebootOnCompletion:$true -Force:$true -SafeModeAdministratorPassword $securePassword`
   6. `Install-ADDSForest -DomainName "podx.ucalpha.com" -NoRebootOnCompletion:$true -SafeModeAdministratorPassword $securePassword -Force:$true`
   6. `Install-ADDSForest -DomainName "podx.ucalpha.com" -SafeModeAdministratorPassword $securePassword -Force:$true`
   5. **Restart Needed, takes a long time**
3. ### Install DNS Services
   5. `Install-WindowsFeature -Name DNS -IncludeManagementTools`;
      `Success Restart Needed Exit Code      Feature Result`
   `------- -------------- ---------      --------------`
   `True    No             Success        {DNS Server, DNS Server Tools}`
   6. #### Configure DNS Zones
      6. `Add-DnsServerPrimaryZone -Name "podx.ucalpha.com" -ZoneFile "podx.ucalpha.com.dns";`
         7. `No Output if sucessful` 
         7. `Might already exist`
         8. `Add-DnsServerPrimaryZone : Failed to create zone podx.ucalpha.com on server DC.` 
         9. `At line:1 char:1`
         9. `+ Add-DnsServerPrimaryZone -Name "podx.ucalpha.com" -ZoneFile "podx.uca ...`
         `+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
         10. `+ CategoryInfo          : ResourceExists: (podx.ucalpha.com:root/Microsoft/...rverPrimaryZone) [Add-DnsServerPrimaryZone], CimException`
         10. `+ FullyQualifiedErrorId : WIN32 9609,Add-DnsServerPrimaryZone`
  7. `Add-DnsServerPrimaryZone -NetworkId "10.89.242.0/24" -ZoneFile "10.89.242.in-addr.arpa.dns";`
     8. No Output if
  8. `Set-DnsServerForwarder -IPAddress "10.89.208.101", "8.8.8.8"`
     9. No Output
4. ### Add DNS Entries
   5. Forward
      * `Add-DnsServerResourceRecordA -Name "testing" -ZoneName "podx.ucalpha.com" -IPv4Address "10.89.242.242"`
      * NO Output
   6. Reverse
      * `Add-DnsServerResourceRecordPtr -Name "242" -ZoneName "242.89.10.in-addr.arpa" -PtrDomainName "testing.podx.ucalpha.com"`
      * No Output
5. ### Install CA
   6. `Install-WindowsFeature -Name ADCS-Cert-Authority,ADCS-Web-Enrollment -IncludeManagementTools`
   `Success Restart Needed Exit Code      Feature Result`
   `------- -------------- ---------      --------------`
   `True    No             Success        {Active Directory Certificate Services, Ce...`
6. ### Configure CA
   **7. Update Values Accordingly**
   7. `Import-Module ADCSDeployment; Install-AdcsCertificationAuthority -CAType EnterpriseRootCA -CACommonName \"podx-DC-CA\" -CADistinguishedNameSuffix \"DC=podx,DC=ucalpha,DC=com\" -KeyLength 4096 -HashAlgorithmName SHA256 -CryptoProviderName \"RSA#Microsoft Software Key Storage Provider\" -ValidityPeriod Years -ValidityPeriodUnits 5 -DatabaseDirectory \"C:\Windows\System32\CertLog\" -LogDirectory \"C:\Windows\System32\CertLog\" -Force`
   8. `Import-Module ADCSDeployment; Install-AdcsCertificationAuthority -CAType EnterpriseRootCA -Force;`
      9. `ErrorId ErrorString`
      `------- -----------`
      `0`
   10. `Install-AdcsWebEnrollment -Force`
       `ErrorId ErrorString`
       `------- -----------`
       `0`
   * Fails Before Reboot.
     * `Install-AdcsCertificationAuthority : Active Directory Certificate Services setup failed with the following error:  A value for the attribute was not in the acceptable range of values. 0x80072082 (WIN32: 8322 ERROR_DS_RANGE_CONSTRAINT)`
7. ### Add AD USERS:
   8. `New-ADUser -Name "Dwight Schrute" -SamAccountName "dschrute" -UserPrincipalName "dchrute@podx.ucalpha.com" -Path "CN=Users,DC=podx,DC=ucalpha,DC=com" -OfficePhone "123-456-7890" -AccountPassword (ConvertTo-SecureString "C0c0a123!" -AsPlainText -Force) -Enabled $true -PasswordNeverExpires $true -ChangePasswordAtLogon $false`