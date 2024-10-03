### Install AD-Domain-Services
   `Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools`<br><br>
   `Success Restart Needed Exit Code Feature Result`<br>
   `------- -------------- ---------      --------------`<br>
   `True    No             Success        {Active Directory Domain Services, Group P...`
### Promote to Domain Controller
   `$securePassword = ConvertTo-SecureString "C0c0a123!" -AsPlainText -Force;`<br>
   **No Output**<br>
   `Import-Module ADDSDeployment; `
   `Install-ADDSForest -DomainName "podx.adanzuniga.com" -NoRebootOnCompletion:$true -SafeModeAdministratorPassword $securePassword -Force:$true;`<br><br>
   **Long restart.** Decide if auto restart, or controlled 
### Install DNS Services
   `Install-WindowsFeature -Name DNS -IncludeManagementTools`;<br><br>
   `Success Restart Needed Exit Code      Feature Result`<br>
   `------- -------------- ---------      --------------`<br>
   `True    No             Success        {DNS Server, DNS Server Tools}`
### Configure DNS Zones
   `Add-DnsServerPrimaryZone -Name "podx.adanzuniga.com" -ZoneFile "podx.adanzuniga.com.dns";`<br>
   No Output if sucessful<br>
   Might already exist<br><br>
   `Add-DnsServerPrimaryZone : Failed to create zone podx.adanzuniga.com on server DC.` <br>
   `At line:1 char:1`<br>
   `+ Add-DnsServerPrimaryZone -Name "podx.adanzuniga.com" -ZoneFile "podx.uca ...`<br>
   `+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`<br>
   `+ CategoryInfo          : ResourceExists: (podx.adanzuniga.com:root/Microsoft/...rverPrimaryZone) [Add-DnsServerPrimaryZone], CimException`<br>
   `+ FullyQualifiedErrorId : WIN32 9609,Add-DnsServerPrimaryZone`<br><br>
   `Add-DnsServerPrimaryZone -NetworkId "10.0.1.0/24" -ZoneFile "10.0.1.in-addr.arpa.dns";`<br>
   No output if successful<br>
   `Set-DnsServerForwarder -IPAddress "8.8.8.8", "8.8.4.4"`<br>
   No output
### Add DNS Entries
   Forward<br>
   `Add-DnsServerResourceRecordA -Name "testing" -ZoneName "podx.adanzuniga.com" -IPv4Address "10.0.1.254"`<br>
   `Add-DnsServerResourceRecordA -Name "cucm1" -ZoneName "podx.adanzuniga.com" -IPv4Address "10.0.1.150"`<br>
   No output<br><br>
   Reverse<br>
   `Add-DnsServerResourceRecordPtr -Name "254" -ZoneName "1.0.10.in-addr.arpa" -PtrDomainName "testing.podx.adanzuniga.com"`<br>
   `Add-DnsServerResourceRecordPtr -Name "150" -ZoneName "1.0.10.in-addr.arpa" -PtrDomainName "cucm1.podx.adanzuniga.com"`<br>
   No Output
### Install CA
   `Install-WindowsFeature -Name ADCS-Cert-Authority,ADCS-Web-Enrollment -IncludeManagementTools`<br>
   `Success Restart Needed Exit Code      Feature Result`<br>
   `------- -------------- ---------      --------------`<br>
   `True    No             Success        {Active Directory Certificate Services, Ce...`<br>
### Configure CA
**Update Values Accordingly**<br>
`Import-Module ADCSDeployment;`<br>
`Install-AdcsCertificationAuthority -CAType EnterpriseRootCA -Force;`<br>
`ErrorId ErrorString`<br>
`------- -----------`<br>
`0`<br><br>
`Install-AdcsWebEnrollment -Force`<br>
`ErrorId ErrorString`<br>
`------- -----------`<br>
`0`<br>
Fails Before Reboot.
`Install-AdcsCertificationAuthority : Active Directory Certificate Services setup failed with the following error:  A value for the attribute was not in the acceptable range of values. 0x80072082 (WIN32: 8322 ERROR_DS_RANGE_CONSTRAINT)`
### Add AD USERS:
`New-ADUser -Name "Dwight Schrute" -SamAccountName "dschrute" -UserPrincipalName "dchrute@podx.adanzuniga.com" -Path "CN=Users,DC=podx,DC=adanzuniga,DC=com" -OfficePhone "123-456-7890" -AccountPassword (ConvertTo-SecureString "C0c0a123!" -AsPlainText -Force) -Enabled $true -PasswordNeverExpires $true -ChangePasswordAtLogon $false`