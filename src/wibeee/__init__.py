import src.wibeee.utils
import requests
# ip = "http://192.168.1.145/"
# url = "http://" + ip + "/services/user/values.xml"


class WiBeee:
    def __init__(self, host=None, port=80, timeout=10.0, ucm='async_httpx'):
        self.host = host
        self.port = port
        self.timeout = timeout
        if not host:
            self.host = self.autoDiscover()

    def callURL(self, url):
        """Call URL function."""
        request = requests.Request("GET", url).prepare()
        try:
            with requests.Session() as sess:
                response = sess.send(
                    request, timeout=self.timeout
                )
            return response.text
        except Exception as e:
            return "Error: " + str(e)

    def autoDiscover(self):
        hosts = utils.getActiveHosts()
        for host in hosts:
            url = "http://{0}:{1}/en/login.html".format(host, self.port)
            result = self.callURL(url)
            if "<title>WiBeee</title>" in result:
                return host
