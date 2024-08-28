# Crypto Chassis Trade
* A pure Python library for trading on cryptocurrency exchanges.
* More than a library, it syncs exchange data to local memory and keeps track of realtime data updates.
* Unified API for different exchanges.
* Super simple to use. Your code will be in a linear and synchronous manner. The library takes care of asynchronous networking.
* Supported exchanges:
  * Okx.
  * More comming soon...
* Public beta. All kinds of feedbacks and contributions are welcomed.
* Join us on Discord https://discord.gg/b5EKcp9s8T and Medium https://cryptochassis.medium.com.

## Branches
* The `main` branch may contain experimental features.
* The `release` branch represents the most recent stable release.

## Installation
* It's recommended that you install in a virtual environment of your choosing.

### Install From PyPi
* `pip install crypto_chassis_trade`.
* For developers, `pip install 'crypto_chassis_trade[dev]'`.

### Install Locally
* `pip install .`.
* For developers, `pip install '.[dev]'`.

## Public API
* [See all methods in class `ExchangeInterface` for public interfaces.](crypto_chassis_trade/core/exchanges/exchange_interface.py)
* [See the `__init__` method in class `ExchangeBase` for public configurations.](crypto_chassis_trade/core/exchanges/exchange_base.py)

## Examples
* [Quick start](examples/quick_start.py)
* [More examples](examples)

## Thread safety
* Single thread.

## Performance Tuning
* [Use a faster json library such as orjson](tests/test_orjson.py).
* [Use a faster event loop such as uvloop](tests/test_uvloop.py).
