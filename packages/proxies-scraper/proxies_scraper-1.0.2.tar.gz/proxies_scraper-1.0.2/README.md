# Proxies Scraper

A Python package for searching free proxies. This package allows you to retrieve and filter proxy servers based on
various criteria such as:
- Country code.
- Anonymity level.
- HTTP or HTTPS type.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Example](#basic-example)
  - [Advanced Example](#advanced-example)
  - [Return Example](#advanced-example)
- [Function Documentation](#function-documentation)
  - [`get_proxies`](#get_proxies)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Proxies Scraper is a versatile Python package designed to help developers find and filter free proxy servers.
It can be particularly useful for tasks such as web scraping, automated testing, and browsing with privacy.

## Features

- Filter proxies by country code.
- Filter proxies by anonymity level.
- Filter proxies by HTTP/HTTPS type.

## Installation

You can install the package using pip:

```sh
pip install proxies_scraper
```

## Usage

### Basic Example

Get a list of all proxies.

```python

from proxies_scraper.main import get_proxies

proxies = get_proxies()

print(proxies)
```

### Advanced Example

Get a proxies list filtered by country code and HTTPS support.

```python

from proxies_scraper.main import get_proxies

proxies = get_proxies(
    country_codes_filter=['US'],
    anonymity_filter=[2],
    https_filter=True
)

print(proxies)
```

### Return Example

The `get_proxies` method will return the results with the following structure:

```JSON
[
    {
        "ip_address": "192.168.1.1",
        "port": "8090",
        "proxy": "192.168.1.1:8090",
        "country_code": "GB",
        "country": null,
        "anonymity": 1,
        "https": false,
        "source": "webpage",
        "last_checked": 1724839341,
        "created_date": "2024-08-28 15:25:01.228439"
    }
]
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Implement your changes and ensure your code passes the tests.
4. Commit your changes with a descriptive commit message.
5. Push your changes to your forked repository.
6. Create a pull request to the main repository.

Please make sure your code adheres to the project's coding standards and includes appropriate tests.
