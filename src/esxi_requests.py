from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings, exceptions
from json import dumps as json_dumps
from bs4 import BeautifulSoup

disable_warnings(exceptions.InsecureRequestWarning)


def looper(kind, collection):
    kind = kind.removeprefix('/redfish/v1/')
    print(f'{" " + kind + " ":#^80}')
    # if item != 'Actions':
    for item in collection:
        print(f'{kind}: {item}')
        print('\t' * 3, collection[item], end='\n')

    print(f'{" " + kind + " ":#^80}', end='\n')


class CIMC:
    def __init__(self, cimc_ip, user, password):
        """
        `CIMC API Examples
        <https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/c/sw/api/3_0/b_Cisco_IMC_REST_API_guide_301/m_redfish_api_examples.html>`_

        `CICM API Guides
        <https://www.cisco.com/c/en/us/support/servers-unified-computing/ucs-c-series-integrated-management-controller/products-programming-reference-guides-list.html>`_

        `Extracting Cookies <https://stackoverflow.com/questions/15778466/using-python-requests-sessions-cookies-and-post>`_
        """
        self._ip = cimc_ip
        self._user = user
        self._password = password
        self._session = Session()
        self._session.auth = HTTPBasicAuth(user, password)
        self._session.verify = False
        # if json:
        #     self._session.headers = {"Accept": "application/json",
        #                              "Content-type": "application/json"}
        self._baseurl = f"https://{self._ip}"
        session_url, session_cookie = self._create_session()
        self.session_url = session_url
        self._session_cookie = session_cookie
        self._session.headers = {"X-Auth-Token": self._session_cookie}

    def _create_session(self):
        # create_session_url = self._baseurl + "/ccmadmin/j_security_check"
        create_session_url = self._baseurl + "/ccmadmin/showHome.do"
        data = {"j_username": self._user,
                "j_password": self._password
                }

        resp = self._session.post(url=create_session_url, data=data)
        print(resp, '\n')
        # print(resp.history)
        # print(resp.content)
        for c in self._session.cookies:
            print(c)
            print(c.name)
        print(resp.headers)
        # print(resp.text)
        self.get_sessions()
        # session_resp_json = resp.json()
        # session_url = session_resp_json['@odata.id']
        # session_name = session_resp_json['Name']
        # session_description = session_resp_json['Description']
        # print(session_name)
        # print(session_description)
        # session_cookie = resp.headers['X-Auth-Token']

        # return session_url, session_cookie
        return True, False

    def get_sessions(self):
        resp = self._session.get(url=self._baseurl + "/ccmadmin/showHome.do", verify=False)
        soup = BeautifulSoup(resp.text, 'html.parser')
        print(soup)
        print(soup.find('input', {'name': 'token'}))
        return resp

    def generic_get(self, suffix):
        api_url = self._baseurl + suffix
        resp = self._session.get(api_url)
        return resp


def main():
    ip = "10.0.1.10"
    user = "appadmin"
    password = 'l4bp$$D'
    c = CIMC(ip, user, password)
    # last_resp = c.get_sessions()
    # print(last_resp.json())
    # last_resp = c.get_sessions('/redfish/v1/Managers/CIMC')
    # print(last_resp.json())
    print(c)

    # cimc = c.generic_get('/redfish/v1/Managers/CIMC')
    # looper('/redfish/v1/Managers/CIMC', cimc.json())
    # manager_4_servers_url = cimc.json()['Links']['ManagerForServers'][0]['@odata.id']
    # systems_resp = c.generic_get(manager_4_servers_url)
    # looper(manager_4_servers_url, systems_resp.json())
    # print(systems_resp.url)
    # man_cimc_net_interfaces_urls = '/redfish/v1/Managers/CIMC/EthernetInterfaces/NICs'
    # network_resp = c.generic_get(man_cimc_net_interfaces_urls)
    # looper(man_cimc_net_interfaces_urls, network_resp.json())


if __name__ == '__main__':
    main()
