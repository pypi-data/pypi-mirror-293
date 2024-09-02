import itertools
import random


class ProxyDealer:
    def __init__(self, proxies):
        """
        Initialize the ProxyDealer with a list of proxies.

        :param proxies: List of proxies
        """
        self.proxies = proxies
        self.proxy_cycle = itertools.cycle(self.proxies)
        self.round_counter = 0

    def get_next_proxy_with_shuffle(self):
        """
        Get the next proxy from the cycle.

        :return: Next proxy in the cycle
        """
        proxy = next(self.proxy_cycle)
        self.round_counter += 1

        # Shuffle the proxies every second round
        if self.round_counter % (len(self.proxies) * 2) == 0:
            self.shuffle_proxies()

        return proxy

    def get_next_proxy_no_shuffle(self):
        """
        Get the next proxy from the cycle without shuffling the proxies.

        :return: Next proxy in the cycle
        """
        return next(self.proxy_cycle)

    def shuffle_proxies(self):
        """
        Shuffle the list of proxies and reset the cycle.
        """
        random.shuffle(self.proxies)
        self.proxy_cycle = itertools.cycle(self.proxies)

    def get_random_proxy(self):
        """
        Get a random proxy from the list.

        :return: Random proxy from the list
        """
        return random.choice(self.proxies)

    def print_proxies(self):
        """
        Print the list of proxies (for debugging purposes).
        """
        print("Proxies:", self.proxies)
