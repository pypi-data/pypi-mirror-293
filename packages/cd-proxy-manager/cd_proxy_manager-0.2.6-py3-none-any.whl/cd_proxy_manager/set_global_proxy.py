import os
import subprocess
import platform


class SysProxy:
    def __init__(self):
        self.system = platform.system().lower()
        self.default_no_proxy = "localhost,127.0.0.1"

    def set_proxy(self, proxy):
        """
        Set the system proxy.

        :param proxy: Proxy server in the format 'proxy:port' or 'proxy:port:username:password'
        """
        if self.system == 'windows':
            self._set_proxy_windows(proxy)
        elif self.system == 'darwin':  # macOS
            self._set_proxy_macos(proxy)
        elif self.system == 'linux':
            self._set_proxy_linux(proxy)
        else:
            raise NotImplementedError(f"Setting proxy not implemented for {self.system}")

    def set_no_proxy(self):
        """
        Set the no-proxy settings to default: "localhost,127.0.0.1"
        """
        if self.system == 'windows':
            self._set_no_proxy_windows()
        elif self.system == 'darwin':  # macOS
            self._set_no_proxy_macos()
        elif self.system == 'linux':
            self._set_no_proxy_linux()
        else:
            raise NotImplementedError(f"Setting no-proxy not implemented for {self.system}")

    def _set_proxy_windows(self, proxy):
        # Set WinHTTP proxy
        command = f"netsh winhttp set proxy {proxy}"
        subprocess.run(command, shell=True)
        # Set WinINET proxy (for browsers and other applications)
        proxy_server = proxy.split(':')[0]
        proxy_port = proxy.split(':')[1]
        internet_settings = f'REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyServer /t REG_SZ /d {proxy_server}:{proxy_port} /f'
        subprocess.run(internet_settings, shell=True)
        proxy_enable = 'REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f'
        subprocess.run(proxy_enable, shell=True)

    def _set_no_proxy_windows(self):
        # Reset WinHTTP proxy
        command = f"netsh winhttp reset proxy"
        subprocess.run(command, shell=True)
        # Reset WinINET proxy
        proxy_disable = 'REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f'
        subprocess.run(proxy_disable, shell=True)
        os.environ['no_proxy'] = self.default_no_proxy

    def _set_proxy_macos(self, proxy):
        proxy_server, proxy_port = proxy.split(':')
        command = [
            'networksetup', '-setwebproxy', 'Wi-Fi', proxy_server, proxy_port
        ]
        subprocess.run(command)
        command = [
            'networksetup', '-setsecurewebproxy', 'Wi-Fi', proxy_server, proxy_port
        ]
        subprocess.run(command)

    def _set_no_proxy_macos(self):
        command = [
            'networksetup', '-setproxybypassdomains', 'Wi-Fi', *self.default_no_proxy.split(',')
        ]
        subprocess.run(command)

    def _set_proxy_linux(self, proxy):
        os.environ['http_proxy'] = proxy
        os.environ['https_proxy'] = proxy
        self._set_global_env('http_proxy', proxy)
        self._set_global_env('https_proxy', proxy)

    def _set_no_proxy_linux(self):
        os.environ['no_proxy'] = self.default_no_proxy
        self._set_global_env('no_proxy', self.default_no_proxy)

    def _set_global_env(self, var, value):
        with open('/etc/environment', 'a') as f:
            f.write(f'{var}="{value}"\n')

