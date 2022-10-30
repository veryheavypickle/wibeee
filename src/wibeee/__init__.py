import src.wibeee.utils
import src.wibeee.errors as errors
import requests
import xmltodict
import time


class WiBeee:
    def __init__(self, host=None, port=80, timeout=10.0, ucm='async_httpx'):
        self.host = host
        self.port = port
        self.timeout = timeout
        if not host:
            self.host = self.autoDiscover()
        self.baseURL = "http://{0}:{1}".format(host, self.port)

    def callURL(self, url):
        """Call URL function."""
        request = requests.Request("GET", url).prepare()
        try:
            with requests.Session() as sess:
                response = sess.send(
                    request, timeout=self.timeout
                )
            return response.text
        except requests.exceptions.Timeout:
            raise errors.BadHostName("The WiBeee device seems to be down, try autodiscovery")
        except requests.exceptions.ConnectionError:
            time.sleep(1)
            return self.callURL(url)

    def autoDiscover(self):
        hosts = utils.getActiveHosts()
        for host in hosts:
            url = self.baseURL + "/en/login.html"
            result = self.callURL(url)
            if "<title>WiBeee</title>" in result:
                return host
        raise errors.NoWiBeeeDevices("No WiBee Devices were found on the local network")

    def getStatus(self):
        url = self.baseURL + "/en/status.xml"
        return xmltodict.parse(self.callURL(url))["response"]
