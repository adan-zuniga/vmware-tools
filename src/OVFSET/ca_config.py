import re
from textwrap import dedent


def install_certificate_services():
    path = r'C:\Windows\system32\WindowsPowerShell\v1.0\powershell.exe -Command'

    # Install-WindowsFeature -Name ADCS-Cert-Authority -IncludeManagementTools;
    # Import-Module ADCSDeployment;

    certificate_services_configuration = dedent(r"""
    Install-AdcsCertificationAuthority
    -CAType EnterpriseRootCA
    -CACommonName \"podx-DC-DNS-TEST-CA\"
    -CADistinguishedNameSuffix \"DC=podx,DC=ucalpha,DC=com\"
    -KeyLength 2048
    -HashAlgorithmName SHA256
    -CryptoProviderName \"RSA#Microsoft Software Key Storage Provider\"
    -ValidityPeriod Years
    -ValidityPeriodUnits 5
    -DatabaseDirectory "C:\Windows\System32\CertLog"
    -LogDirectory "C:\Windows\System32\CertLog"
    -Force;
    """).strip()
    # Add-WindowsFeature Adcs-Web-Enrollment;
    # Install-AdcsWebEnrollment -Force
    #

    certificate_services_configuration = certificate_services_configuration.replace('\n', ' ')
    # Replace multiple spaces with a single space
    certificate_services_configuration = re.sub(r'\s{2,}', ' ', certificate_services_configuration)

    # print(f'{path} "& {certificate_services_configuration}"')
    print(certificate_services_configuration)

if __name__ == '__main__':
    install_certificate_services()