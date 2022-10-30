import src.wibeee.utils
import src.wibeee.errors as errors
import requests
import xmltodict
import time


class WiBeee:
    def __init__(self, host=None, port=80, timeout=10.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        if not host:
            self.host = self.autoDiscover()
        self.baseURL = "http://{0}:{1}".format(host, self.port)

    def callURL(self, url, attempts=1):
        """Call URL function."""
        request = requests.Request("GET", url).prepare()
        if attempts > 10:
            raise errors.TooManyAttempts("Multiple attempts to connect to the device failed")
        try:
            with requests.Session() as sess:
                response = sess.send(
                    request, timeout=self.timeout
                )
            return response.text
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            time.sleep(1)
            return self.callURL(url, attempts + 1)
        except requests.exceptions.Timeout as e:
            print(e.response)
            raise errors.BadHostName("The WiBeee device seems to be down, try autodiscovery to get the correct url")

    def autoDiscover(self):
        hosts = utils.getActiveHosts()
        for host in hosts:
            url = self.baseURL + "/en/login.html"
            result = self.callURL(url)
            if "<title>WiBeee</title>" in result:
                return host
        raise errors.NoWiBeeeDevices("No WiBee Devices were found on the local network")

    def getHost(self):
        return self.host

    def getStatus(self):
        url = self.baseURL + "/en/status.xml"
        return xmltodict.parse(self.callURL(url))["response"]

    def voltage(self, phase=1):
        # rms is root-mean-square
        key = "fase{}_vrms".format(phase)
        return float(self.getStatus()[key])

    def current(self, phase=1):
        key = "fase{}_irms".format(phase)
        return float(self.getStatus()[key])

    def frequency(self, phase=1):
        key = "fase{}_frecuencia".format(phase)
        return float(self.getStatus()[key])

    def power(self, phase=1):
        key = "fase{}_p_activa".format(phase)
        return float(self.getStatus()[key])
