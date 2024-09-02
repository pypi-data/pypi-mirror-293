import os


class EnvProxyManager:
    def __init__(self):
        self.proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'FTP_PROXY', 'NO_PROXY']

    @staticmethod
    def set_proxy(http_proxy=None, https_proxy=None, ftp_proxy=None, no_proxy=False):
        """Sets the proxy environment variables."""
        if http_proxy:
            os.environ['HTTP_PROXY'] = http_proxy
        if https_proxy:
            os.environ['HTTPS_PROXY'] = https_proxy
        if ftp_proxy:
            os.environ['FTP_PROXY'] = ftp_proxy
        if no_proxy:
            os.environ['NO_PROXY'] = ""

    def get_proxies(self):
        """Returns a dictionary of the current proxy settings."""
        return {var: os.environ.get(var, 'Not set') for var in self.proxy_vars}

    def print_proxies(self):
        """Prints the current proxy settings."""
        for var in self.proxy_vars:
            print(f"{var}: {os.environ.get(var, 'Not set')}")
