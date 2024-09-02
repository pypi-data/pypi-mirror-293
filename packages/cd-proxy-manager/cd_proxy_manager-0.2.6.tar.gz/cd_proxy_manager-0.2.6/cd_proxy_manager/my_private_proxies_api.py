import requests


class MyPrivateProxyAPI:
    def __init__(self, api_key: str):
        """
        Initialize the MyPrivateProxyAPI class with the provided API key.

        :param api_key: Your API key for accessing the proxy API.
        """
        self.api_key = api_key
        self.base_url = "https://api.myprivateproxy.net/v1"

    def fetch_proxies(self, format_type="plain", output_type="full", proxy_plan_id=None, show_location=False, show_plan_id=False):
        """
        Fetch the list of proxies with optional parameters for format, output type, and additional details.

        :param format_type: The format of the output ('plain' or 'json').
        :param output_type: The type of output ('full' or 'brief').
        :param proxy_plan_id: Optional, filter proxies by proxy plan ID.
        :param show_location: Optional, show details of proxy locations.
        :param show_plan_id: Optional, show proxy plan ID for each proxy.
        :return: The list of proxies in the requested format.
        """
        url = f"{self.base_url}/fetchProxies/{format_type}/{output_type}"
        if proxy_plan_id:
            url += f"/{proxy_plan_id}"
        if show_location:
            url += "/showLocation"
        if show_plan_id:
            url += "/showPlanId"
        url += f"/{self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json() if format_type == "json" else response.text

    def enable_auto_renew(self, proxy_plan_id: str):
        """
        Enable automatic proxy refresh for a specific proxy plan.

        :param proxy_plan_id: The ID of the proxy plan to enable auto-renew.
        :return: The result of the operation.
        """
        url = f"{self.base_url}/enableAutoRenew/{proxy_plan_id}/{self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def disable_auto_renew(self, proxy_plan_id: str):
        """
        Disable automatic proxy refresh for a specific proxy plan.

        :param proxy_plan_id: The ID of the proxy plan to disable auto-renew.
        :return: The result of the operation.
        """
        url = f"{self.base_url}/disableAutoRenew/{proxy_plan_id}/{self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def proceed_proxies_refresh(self, proxy_plan_id: str):
        """
        Initiate immediate proxy change (refresh) for a specific proxy plan.

        :param proxy_plan_id: The ID of the proxy plan to refresh.
        :return: The result of the operation.
        """
        url = f"{self.base_url}/doRenew/{proxy_plan_id}/{self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def specific_proxies_refresh(self, proxy_plan_id: str, proxies: list):
        """
        Initiate immediate proxy change (refresh) for specific proxies in a proxy plan.

        :param proxy_plan_id: The ID of the proxy plan.
        :param proxies: A list of proxies to refresh.
        :return: The result of the operation in JSON format.
        """
        url = f"{self.base_url}/doSpecificRefresh/{self.api_key}"
        response = requests.post(url, json=proxies)
        response.raise_for_status()
        return response.json()

    def fetch_authorized_ips(self):
        """
        Fetch the list of authorized IPs.

        :return: The list of authorized IPs.
        """
        url = f"{self.base_url}/fetchAuthIP/{self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def update_authorized_ips(self, ips: list):
        """
        Replace the current authorized IP list with a new list.

        :param ips: A list of IP addresses to authorize.
        :return: The result of the operation in JSON format.
        """
        url = f"{self.base_url}/updateAuthIP/{self.api_key}"
        response = requests.post(url, json=ips)
        response.raise_for_status()
        return response.json()

    def add_authorized_ips(self, ips: list):
        """
        Add IP addresses to the current authorized IP list.

        :param ips: A list of IP addresses to add to the authorization list.
        :return: The result of the operation in JSON format.
        """
        url = f"{self.base_url}/addAuthIP/{self.api_key}"
        response = requests.post(url, json=ips)
        response.raise_for_status()
        return response.json()

    def remove_authorized_ips(self, ips: list):
        """
        Remove IP addresses from the authorized IP list.

        :param ips: A list of IP addresses to remove from the authorization list.
        :return: The result of the operation in JSON format.
        """
        url = f"{self.base_url}/removeAuthIP/{self.api_key}"
        response = requests.post(url, json=ips)
        response.raise_for_status()
        return response.json()
