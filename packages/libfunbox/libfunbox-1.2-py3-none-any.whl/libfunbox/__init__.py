__lib__: str = "libfunbox"
__version__: float = 1.02


import requests, sys

class Funbox:
    """
    This is a python Funbox 2.0 API, this has no guarantee to work.
    
    This unlocks you to also port forward any protocol you'd like, as the web gui only allows you to choose tcp, udp, or both, here you can enter the IP protocol numbers: https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers
    
    Use at your own risk, am not responsible for any damage done to your modem
    """
    def __init__(self, password: str, base_url:str="192.168.1.1", https:bool=False) -> None:
        self.__base_url = base_url
        
        self.__session = requests.Session()
        self.__session.headers.update({"Content-Type": "application/x-sah-ws-1-call+json; charset=UTF-8"})
        self.__session.headers.update({"Connection": "keep-alive"})
        self.__session.headers.update({"X-Requested-With": "XMLHttpRequest"})
        self.__session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"})
        self.__protocol = "https" if https else "http"
        self.__session.headers.update({"Origin": f"{self.__protocol}://{base_url}"})
        
        auth = self.__session.post(f"{self.__protocol}://{base_url}/authenticate?username=admin&password={password}")
        if auth.status_code == 401: raise PermissionError("Invalid password")
        self.__session.headers.update({"X-Context": auth.json()["data"]["contextID"]})
        
        self.__authenticated = True
        self.__password__ = password
    def _reauthenticate(self) -> None:
        auth = self.__session.post(f"{self.__protocol}://{self.__base_url}/authenticate?username=admin&password={self.__password__}")
        if auth.status_code == 401: raise PermissionError("Invalid password")
        self.__session.headers.update({"X-Context": auth.json()["data"]["contextID"]})
    def _get(self, path: str, headers={}) -> requests.Response:
        assert self.__authenticated
        return self.__session.get(f"{self.__protocol}://{self.__base_url}/{path}", headers=headers)
    def _post(self, path: str, parameters={}, headers={}) -> requests.Response:
        assert self.__authenticated
        return self.__session.post(f"{self.__protocol}://{self.__base_url}/{path}", json={"parameters": parameters}, headers=headers)
    
    def GetVoIPTrunks(self) -> dict:
        """
        This returns a list of available VoIP trunks, each object has a name, signaling protocol, is it disabled or not, trunk lines and signaling protocol details
        """
        return self._post("sysbus/VoiceService/VoiceApplication:listTrunks").json()["result"]["status"]
    def GetVoIPConfig(self) -> dict:
        """
        This returns a list of the ways that the trunks are connected
        """
        return self._post("sysbus/NMC:getVoIPConfig").json()["result"]["status"]
    
    def GetAllConnectedDevices(self) -> dict:
        """
        This returns every device connected to the modem, such as usb, wifi and eth
        """
        return self._post("sysbus/Devices:get", {"expression":{"usbM2M":" usb && wmbus and .Active==true","usb":" printer && physical and .Active==true","usblogical":"volume && logical and .Active==true","wifi":"(wifi and (edev || wifi_bridge) and .Active == true)","eth":"(eth and (edev || wifi_bridge) and .Active == true)","dect":"voice && dect && handset && physical"}}).json()["result"]["status"]
    def GetUSBDevices(self):
        """
        This returns every USB device connected, i don't know the format of this
        """
        return self._post("sysbus/Devices:get", {"expression":{"usb":"volume && logical and .Active==true"}}).json()["result"]["status"]["usb"]
    def GetWANStatus(self) -> dict:
        """
        This returns your current link type, current protocol, connection errors, remote gateway
        """
        return self._post("sysbus/NMC:getWANStatus").json()["result"]["data"]
    def GetPPPUsername(self) -> str:
        """
        Returns your PPP username
        """
        return self._post("sysbus/NeMo/Intf/data:getFirstParameter", {"name":"Username","flag":"ppp || dhcp","traverse":"down"}).json()["result"]["status"]
    def IsLinkUp(self) -> bool:
        """
        Returns a boolean, signaling if your link is up
        """
        return self._post("sysbus/NeMo/Intf/dsl0:getFirstParameter", {"name": "LinkStatus"}).json()["result"]["status"] == "Up"
    def GetIPv4(self) -> str | None:
        """
        Returns your current IPv4 address
        """
        if not self.IsLinkUp():
            return None
        return self._post("sysbus/NeMo/Intf/data:luckyAddrAddress", {"flag": "ipv4 && global"}).json()["result"]["status"]
    def GetIPv6(self) -> str | None:
        """
        Returns your current IPv6 address
        """
        if not self.IsLinkUp():
            return None
        res = self._post("sysbus/NMC/IPv6:get").json()["result"]["data"]["IPv6Address"]
        return res if res != "" else None
    def GetDSLLinkDetails(self) -> dict:
        """To me, this is the most intresting endpoint, here it provides this:
        
        List of DSL connections, inside of each dsl connection we have these:
        
        CurrentProfile (example '17a')
        DataPath (example 'Interleaved')
        DownstreamAttenuation (example 323) - Not sure, but its probably in db
        DownstreamCurrRate (example 68538) - Link speed, this number is gonna be your max internet speed, its also in kbit/s
        DownstreamMaxRate (example 79854000) - Max link speed, name seems self-explanatory but, 80 gbit/s on a fucking 2 pin line?
        DownstreamNoiseMargin (example 102) - Noise margin, divide by 10 to get amount in db
        DownstreamPower (example 145) - Probably similiar story (thats 1.4 db snr, bruh) [See UpstreamPower]
        FirmwareVersion (example '4132707636463033396a2e6432346e00') - Modem firmware version? (modem like the internal modem, the router has a modem in it)
        InterleaveDepth (example 0)
        LastChange (example 322650)
        LastChangeTime (example 93882)
        LinkStatus (example 'Up') - You can get this with IsLinkUp()
        ModulationHint (example 'Auto')
        ModulationType (example 'VDSL')
        StandardUsed (example '993.2_Annex_B')
        StandardsSupported (example 'G.992.1_Annex_A, G.992.1_Annex_B, ...') - The elipsis was added by me, this is basicly a list with supported standards, with a ', ' in between each
        UPBOKLE (example 127)
        UpstreamAttenuation (example 154)
        UpstreamCurrRate (example 8566) - Your upload speed
        UpstreamMaxRate (example 9442000)
        UpstreamNoiseMargin (example 86)
        UpstreamPower (example -72) - or is it dbm? idk
        """
        
        return self._post("sysbus/NeMo/Intf/data:getMIBs", {"mibs":"dsl","flag":"","traverse":"down"}).json()["result"]["status"]["dsl"]
    def GetPPPInfo(self) -> dict:
        """
        This has your PPP connection data, such as your username, connection status, connection errors, MRU size, PPP session id, remote gateway, local (public) ip address
        """
        return self._post("sysbus/NeMo/Intf/data:getMIBs",{"mibs":"base ppp dhcp","flag":"ppp || dhcp","traverse":"down"}).json()["result"]["status"]["ppp"]["ppp_data"]
    def GetInternetMTU(self) -> int:
        """
        Returns MTU
        """
        return self._post("sysbus/NeMo/Intf/data:getFirstParameter", {"name":"MTU"}).json()["result"]["status"]
    def GetUsers(self) -> dict:
        """
        This contains all the users that the modem has
        """
        return self._post("sysbus/UserManagement:getUsers").json()["result"]["status"]
    def GetModemInfo(self) -> dict:
        """Get information about your modem, such as:
            Manufacturer
            ManufacturerOUI (?)
            ModelName
            Description
            ProductClass
            SerialNumber
            HardwareVersion
            SoftwareVersion
            RescueVersion
            ModemFirmwareVersion
            EnabledOptions (?)
            AdditionalHardwareVersion
            AdditionalSoftwareVersion
            SpecVersion
            ProvisioningCode
            UpTime
            FirstUseDate (not valid)
            DeviceLog (?)
            VendorConfigFileNumberOfEntries (?)
            ManufacturerURL
            Country
            ExternalIPAddress
            DeviceStatus
            NumberOfReboots (not valid)
        """
        return self._get("sysbus/DeviceInfo").json()["parameters"]
    def GetStatusLEDsState(self) -> dict:
        """
        Get LEDs, upgrade led doesn't exist, lan led is wan port led
        """
        return self._post("sysbus/LED:getAllLedStatus").json()["result"]["data"]["statusList"]
    def GetModemMACAddress(self) -> str:
        """
        Returns modem's mac address
        """
        return self._post("sysbus/NeMo/Intf/lan:getFirstParameter", {"name":"LLAddress"}).json()["result"]["status"]
    def GetLANIPAddress(self) -> dict:
        """
        Returns the modem's lan ip, alongside with its network mask, dhcp toggle, dhcp min and max addresses
        """
        return self._post("sysbus/NMC:getLANIP").json()["result"]["data"]
    def SetLANIPAddrress(self, modem_ip_addres: str, netmask: str, dhcp: bool, dhcp_min_address: str, dhcp_max_address: str) -> None:
        """
        Set the modem ip, netmask or dhcp min/max address
        """
        assert self._post("sysbus/NMC:setLANIP", {"Address":modem_ip_addres,"Netmask":netmask,"DHCPEnable":dhcp,"DHCPMinAddress":dhcp_min_address,"DHCPMaxAddress":dhcp_max_address})
    def GetIPv6ConnectionDetails(self) -> dict:
        """
        Details about the IPv6 connection, like is it enabled, is IPv4 forces and the IPv6 address itself
        """
        return self._post("sysbus/NMC/IPv6:get").json()["result"]["data"]
    def SetWanMode(self, dsl: bool) -> None:
        """
        Sets the WAN mode, this is a toggle between using VDSL or the WAN ethernet port
        """
        assert self._post("sysbus/NMC:setWanMode", {"WanMode":"VDSL_PPP" if dsl else "Ethernet_PPP"}).json()["result"]["status"]
    def RestartConnection(self) -> None:
        """
        Restarts the connection
        """
        def DisableConnection():
            nonlocal self
            self._post("sysbus/NeMo/Intf/data:setFirstParameter", {"name":"Enable","value":0,"flag":"ppp","traverse":"down"})
        def StartConnection():
            nonlocal self
            self._post("sysbus/NeMo/Intf/data:setFirstParameter", {"name":"Enable","value":1,"flag":"ppp","traverse":"down"})
        DisableConnection()
        StartConnection()
    
    def IsWifiOn(self) -> bool:
        return self._post("sysbus/NMC/Wifi:get").json()["result"]["status"]["Status"]
    def GetWiFiOptions(self) -> dict:
        return self._post("sysbus/NeMo/Intf/lan:getMIBs",{"mibs": "wlanradio"}).json()["result"]["status"]
    def GetWiFiBytes(self) -> dict:
        """
        Returns RxBytes and TxBytes of WiFi
        """
        return self._post("sysbus/NMC/Wifi:getStats").json()["result"]["data"]
    def GetWiFiOpenModeStatus(self) -> dict:
        return self._post("sysbus/Wificom/OpenMode:getStatus").json()["result"]["data"]
    def SetWiFiOn(self, value: bool) -> None:
        """
        Turn wifi on and off
        
        TODO: Get successfull response
        """
        self._post("sysbus/NMC/Wifi:set", {"Enable":value,"Status":value})
    
    def GetIPTVStatus(self) -> bool:
        """
        Is IPTV working?
        """
        return self._post("sysbus/NMC/OrangeTV:getIPTVStatus").json()["result"]["data"]["IPTVStatus"] == "Available"
    def GetIPTVChannels(self) -> dict:
        return self._post("sysbus/NMC/OrangeTV:getIPTVConfig").json()["result"]["status"]
    
    def GetDHCPStaticLeases(self) -> dict:
        """
        Returns every ip address and mac address of any static ip device
        """
        return self._post("sysbus/DHCPv4/Server/Pool/default:getStaticLeases").json()["result"]["status"]
    def GetDHCPActiveDevices(self) -> dict:
        """
        Get devices which are currently using DHCP and are connected
        """
        return self._post("sysbus/Devices:get", {"expression":"edev && physical && dhcp and .Active==true"}).json()["result"]["status"]
    def GetDHCPUnActiveDevices(self) -> dict:
        """
        Get devices which aren't currently using DHCP and aren't connected
        """
        return self._post("sysbus/Devices:get", {"expression":".Active==false","traverse":"down","flags":""}).json()["result"]["status"]
    def AddDHCPStaticLease(self, mac_address: str, ip_address: str) -> None:
        """
        Add a DHCP static lease
        """
        assert self._post("sysbus/DHCPv4/Server/Pool/default:addStaticLease", {"MACAddress":mac_address.upper(),"IPAddress":ip_address}).status_code == 200
    def RemoveDHCPStaticLease(self, mac_address: str) -> None:
        """
        Remove a DHCP lease
        """
        assert self._post("sysbus/DHCPv4/Server/Pool/default:deleteStaticLease", {"MACAddress":mac_address.lower()}).status_code == 200
    
    def GetForwardedPorts(self) -> dict:
        """
        Get currently forwarded ports either normally or with UPnP
        """
        return self._post("sysbus/Firewall:getPortForwarding").json()["result"]["status"]
    def PortForward(self, service_name: str, ip_protocol_numbers: list, ip: str, internal_port: int, external_port: int) -> None:
        """
        Forward a port
        
        Please commit after creating your ports with FirewallCommit()
        
        :param service_name: Friendly name for the service
        :param ip_protocol_numbers: The protocol that you want that port to forward, see https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers
        :param internal_port: Where to send the traffic
        :param external_port: Where to get the traffic
        """
        assert self._post("sysbus/Firewall:setPortForwarding", {"description":service_name,"persistent":True,"enable":True,"protocol":",".join(ip_protocol_numbers),"destinationIPAddress":ip,"internalPort":str(internal_port),"externalPort":str(external_port),"origin":"webui","sourceInterface":"data","sourcePrefix":"","id":service_name}).json()["result"]["status"] == f"webui_{service_name}"
    def DisablePortForward(self, service_name: str, ip_protocol_numbers: list, ip:str, internal_port: int, external_port: int) -> None:
        """
        See PortForward()
        """
        assert self._post("sysbus/Firewall:setPortForwarding", {"description":service_name,"persistent":True,"enable":False,"protocol":",".join(ip_protocol_numbers),"destinationIPAddress":ip,"internalPort":str(internal_port),"externalPort":str(external_port),"origin":"webui","sourceInterface":"data","sourcePrefix":"","id":service_name}).json()["result"]["status"] == f"webui_{service_name}"
    def ReEnablePortForward(self, service_name: str, ip_protocol_numbers: list, ip:str, internal_port: int, external_port: int) -> None:
        """
        See PortForward()
        """
        assert self._post("sysbus/Firewall:setPortForwarding", {"description":service_name,"persistent":True,"enable":True,"protocol":",".join(ip_protocol_numbers),"destinationIPAddress":ip,"internalPort":str(internal_port),"externalPort":str(external_port),"origin":"webui","sourceInterface":"data","sourcePrefix":"","id":service_name}).json()["result"]["status"] == f"webui_{service_name}"
    def DeletePortForward(self, service_name: str, ip_protocol_numbers: list, internal_port: int, external_port: int) -> None:
        """
        See PortForward()
        """
        assert self._post("sysbus/Firewall:setPortForwarding", {"description":service_name,"persistent":True,"enable":False,"protocol":",".join(ip_protocol_numbers),"destinationIPAddress":"0.0.0.0","internalPort":str(internal_port),"externalPort":str(external_port),"origin":"webui","sourceInterface":"data","sourcePrefix":"","id":service_name}).json()["result"]["status"] == f"webui_{service_name}"

    def GetUPnPStatus(self) -> dict:
        """
        Is UPnP enabled? what are its details?
        """
        return self._get("sysbus/UPnP-IGD").json()["parameters"]
    def EnableUPnP(self) -> None:
        """
        Please commit after this
        """
        assert self._post("sysbus/UPnP-IGD?_restAction=put", {"Enable":"1"}).status_code == 200
    def DisableUPnP(self) -> None:
        """
        Please commit after this
        """
        assert self._post("sysbus/UPnP-IGD?_restAction=put", {"Enable":"0"}).status_code == 200
    def GetUPnPForwardedPorts(self) -> dict:
        """
        Get currently forwarded ports with UPnP
        """
        return self._post("sysbus/Firewall:getPortForwarding", {"origin": "upnp"}).json()["result"]["status"]
    
    def FirewallCommit(self) -> None:
        assert self._post("sysbus/Firewall:commit").json()["result"]["status"] == True

    def GetFirewallLevel(self) -> str:
        return self._post("sysbus/Firewall:getFirewallLevel").json()["result"]["status"]
    def SetFirewallLevel(self, level: str) -> None:
        """
        Available levels are:
        'Low'
        'Medium'
        'High'
        'Custom'
        """
        assert self._post("sysbus/Firewall:setFirewallLevel", {"level": level}).json()["result"]["status"] == True
    def GetFirewallCustomRespondToPing(self) -> bool:
        """
        Do we wanna respond to ping from the internet?
        """
        res = self._post("sysbus/Firewall:getRespondToPing", {"sourceInterface": "data"}).json()["result"]["status"]
        return (res["enableIPv4"] and res["enableIPv6"])
    def SetFirewallCustomRespondToPing(self, value: bool) -> None:
        assert self._post("sysbus/Firewall:setRespondToPing", {"sourceInterface":"data","service_enable":{"enableIPv4":value,"enableIPv6":value}}).json()["result"]["status"]
    def GetFirewallCustomRules(self) -> None:
        return self._post("sysbus/Firewall:getCustomRule", {"chain":"Custom"}).json()["result"]["status"]
    def AddFirewallCustomRule(self, service_name: str, action: str, destination_port, source_port, protocols: list) -> None:
        """Commit after creating a port
        
        :param action: either 'Accept' or 'Drop'
        :param destination_port: This needs to be range, for example 80-80 6666-6667, or can be ''
        :param source_port: This needs to be range, for example 80-80 6666-6667, or can be ''
        """
        assert self._post("sysbus/Firewall:setCustomRule", {"action":action,"destinationPort":destination_port,"destinationPrefix":None,"sourcePort":source_port,"sourcePrefix":None,"description":service_name,"ipversion":4,"enable":True,"persistent":True,"chain":"Custom","id":service_name,"protocol":",".join(protocols)}).json()["result"]["status"] == service_name
    def RemoveFirewallCustomRule(self, service_name: str, action: str, destination_port, source_port, protocols: list) -> None:
        """Commit after creating a port
        
        :param action: either 'Accept' or 'Drop'
        :param destination_port: This needs to be range, for example 80-80 6666-6667, or can be ''
        :param source_port: This needs to be range, for example 80-80 6666-6667, or can be ''
        """
        assert self._post("sysbus/Firewall:setCustomRule", {"id":service_name,"action":action,"destinationPort":destination_port,"destinationPrefix":"","sourcePort":source_port,"sourcePrefix":"","description":service_name,"protocol":",".join(protocols),"ipversion":0,"enable":False,"persistent":True}).json()["result"]["status"] == service_name
    
    def GetDynamicDNSServices(self) -> list:
        """
        Returns a list of every provider that's supported
        """
        return self._post("sysbus/DynDNS:getServices").json()["result"]["status"]
    def GetDynamicDNSDomains(self) -> list:
        """
        Returns a list of domains
        """
        return self._post("sysbus/DynDNS:getHosts").json()["result"]["status"]
    def AddDynamicDNSDomain(self, service: str, domain: str, username: str, password: str) -> None:
        """
        Adds a domain to be refreshed
        
        :param service: Service, see GetDynamicDNSServices
        :param domain: The domain itself
        :param username: Username or email
        :param password: Account password
        """
        assert self._post("sysbus/DynDNS:addHost", {"hostname":domain,"username":username,"password":password,"service":service}).json()["result"]["status"] == True
    def DeleteDynamicDNSDomain(self, domain: str) -> None:
        """
        Adds a domain to be refreshed
        
        :param domain: The domain itself
        """
        assert self._post("sysbus/DynDNS:delHost", {"hostname":domain}).json()["result"]["status"] == True

    def GetDMZ(self) -> dict:
        """
        Is there currently DMZ?
        """
        res = self._post("sysbus/Firewall:getDMZ").json()["result"]["status"]
        return res if res != {} else None
    def SetDMZ(self, ip_address: str) -> None:
        """
        Set up DMZ
        """
        if not self.GetDMZ() is None: raise Exception("Delete the existing DMZ please")
        assert self._post("sysbus/Firewall:setDMZ", {"id":"webui","sourceInterface":"data","destinationIPAddress":ip_address,"enable":True}).json()["result"]["status"] == "webui"
    def DeleteDMZ(self) -> None:
        """
        Delete the current DMZ
        """
        assert self._post("sysbus/Firewall:deleteDMZ", {"id": "webui"}).json()["result"]["status"] == True
    
    def GetLocalTimeZone(self) -> str:
        """
        See SetLocalTimeZone
        """
        return self._post("sysbus/Time:getLocalTimeZoneName").json()["result"]["data"]["timezone"]
    def SetLocalTimeZone(self, time_zone: str) -> None:
        """
        Available time zones:
            International Date Line West
            Midway Island, Samoa
            Hawaii
            Alaska
            Pacific Time (US/Canada), Tijuana
            Arizona
            Mountain Time (US/Canada)
            Chihuahua, Mazatlan
            Central America
            Central Time (US/Canada)
            Guadalajara, Mexico City, Monterrey
            Saskatchewan
            Bogota, Lima, Quito
            Eastern Time (US/Canada)
            Indiana (East)
            Atlantic Time (Canada)
            Caracas, La Paz
            Santiago
            Newfoundland
            Brasilia
            Buenos Aires, Georgetown
            Greenland
            Mid-Atlantic
            Azores, Cape Verde Is.
            Casablanca, Lisbon, Monrovia
            GMT: Dublin, Edinburgh, London
            Amsterdam, Bern, Rome, Stockholm
            Belgrade, Berlin, Budapest, Ljubljana
            Brussels, Copenhagen, Madrid
            Paris
            Bratislava, Prague, Vienna
            Sarajevo, Skopje, Warsaw, Zagreb
            West Central Africa
            Bucharest, Cairo
            Harare, Pretoria
            Helsinki, Kyiv, Riga, Sofia, Tallinn, Vilnius
            Jerusalem
            Baghdad, Kuwait, Riyadh
            Moscow, St. Petersburg, Volgograd
            Nairobi
            Tehran
            Abu Dhabi, Muscat
            Baku, Tbilisi, Yerevan
            Kabul
            Ekaterinburg
            Islamabad, Karachi, Tashkent
            Chennai, Kolkata, Mumbai, New Delhi
            Kathmandu
            Almaty, Novosibirsk
            Astana, Dhaka
            Rangoon
            Bangkok, Hanoi, Jakarta
            Krasnoyarsk
            Beijing, Chongqing, Hong Kong, Urumqi
            Irkutsk, Ulaan Bataar
            Kuala Lumpur, Singapore
            Perth, Taipei
            Osaka, Sapporo, Tokyo
            Seoul, Yakutsk
            Adelaide, Darwin
            Brisbane
            Canberra, Melbourne, Sydney
            Guam, Port Moresby
            Hobart, Vladivostok
            Magadan, Solomon Is., New Caledonia
            Auckland, Wellington
            Fiji, Kamchatka, Marshall Is.
        """
        assert self._post("sysbus/Time:setLocalTimeZoneName", {"timezone":time_zone}).json()["result"]["status"] == True
    def GetTime(self) -> str:
        return self._post("sysbus/Time:getTime").json()["result"]["data"]["time"]
    
    def SetupRemoteAccess(self, username: str, password: str, port: int) -> None:
        assert self._post("sysbus/NMC:enableRemoteAccess", {"username":username,"password":password,"port":str(port),"timeout":0}).json()["result"]["status"] == port
    def DisableRemoteAccess(self) -> None:
        assert self._post("sysbus/RemoteAccess:disable").json()["result"]["status"] == True
    
    
    def restart(self) -> None:
        """
        This will restart your modem, like turning the power off and on
        """
        assert self._post("sysbus/NMC:reboot").json()["result"]["status"]
    def backup(self) -> tuple[str, bytes]:
        res = self._get("backup?nocache")
        file_name = res.headers["content-disposition"].removeprefix("attachment; filename=")
        return file_name, res.content
    def logout(self) -> None:
        self._get("logout")
        self.__authenticated = False
    def __del__(self):
        if sys.meta_path:
            self.logout()