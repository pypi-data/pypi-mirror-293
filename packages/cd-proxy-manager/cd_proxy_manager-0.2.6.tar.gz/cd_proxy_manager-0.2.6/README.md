# cd_proxy_manager

`cd_proxy_manager` is a Python package designed to handle proxy configurations and management for various purposes such as setting environment proxies, formatting proxies, and dealing with proxies in HTTP requests and browsers.

## Installation

To install `cd_proxy_manager`, clone the repository and install the required dependencies:

```sh
git clone <repository-url>
cd cd_proxy_manager
pip install -r requirements.txt
```
or

```bash
pip install cd-proxy-manager
```
## Modules

### `__init__.py`
This file initializes the package.

### `browser_judges.py`
This module includes various browser judge urls.

### `format_proxy.py`
This module provides functionality for formatting proxies in various formats, making them suitable for use with different libraries and tools.

### `http_judges.py`
This module includes various HTTP judge urls.

### `proxy_dealer.py`
This module is designed to manage and deal with multiple proxies, possibly including rotation and validation.

### `set_env_proxy.py`
This module provides a function to set an environment variable for a proxy, supporting both simple and authenticated proxies.

### `set_global_proxy.py`
This module includes functionality to set a global proxy configuration for the system.

### `version.py`
This module defines the version of the `cd_proxy_manager` package.

### `examples/`
This directory contains example scripts demonstrating how to use the various functionalities provided by the package.

## Usage

### Formatting Proxies

To format a proxy, see example in the examples folder.


### Setting Environment Proxy

To set an environment proxy, use the `set_env_proxy.py` module:

```python
from cd_proxy_manager import SysProxy

# Example: setting a proxy environment variable
proxy = "proxy:port"
SysProxy().set_proxy(proxy)
```

### Proxy Management

To manage multiple proxies, use the `proxy_dealer.py` module:

```python
from cd_proxy_manager import ProxyDealer

# Example: rotating proxies
dealer = ProxyDealer(["proxy1:port", "proxy2:port"])
proxy = dealer.get_next_proxy_no_shuffle()
print(proxy)
```


## See all Examples

Refer to the `examples/` directory for more detailed usage examples.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License.

For more information, visit [codedocta.com](https://codedocta.com).


