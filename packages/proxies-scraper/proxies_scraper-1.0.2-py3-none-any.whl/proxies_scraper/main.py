# main.py
from proxies_scraper.adapters.implementations.freeProxyList import FreeProxyList
from proxies_scraper.adapters.implementations.geonode import Geonode
from proxies_scraper.core.proxy_scraper import ProxyScraper
from proxies_scraper.utils.file_operation import FileOperations
from proxies_scraper.utils.logger import Logger
from proxies_scraper.utils.timer import Timer

# Set logger:
logger = Logger(
    module=FileOperations.get_file_name(__file__, False),
    level="INFO",
)  # Set in configuration file


@Timer(logger=logger, text="Proxies found in {:.2f} seconds\n")
def get_proxies(
    country_codes_filter: list[str] | None = None,
    anonymity_filter: list[int] | None = None,
    https_filter: bool | None = None,
) -> list[dict]:
    """Retrieve a list of proxies based on the provided filters.

    :param country_codes_filter: A list of country codes to filter proxies by location. A country code has two character
    format like 'CA'.
    :type country_codes_filter: list, optional
    :param anonymity_filter: A list of anonymity levels to filter proxies. The values allowed are:
    - 1: Elite proxy
    - 2: Anonymous proxy
    - 3: Transparent proxy
    :type anonymity_filter: list, optional
    :param https_filter: If True, only HTTPS proxies are returned.
    :type https_filter: bool, optional
    :return: A list of proxies matching the specified filters. Each proxy is represented as a dictionary with the
    following keys:
             - `ip` (str): The IP address of the proxy.
             - `port` (int): The port number of the proxy.
             - `country_code` (str): The country code of the proxy.
             - `country` (str): The country of the proxy.
             - `anonymity` (str): The anonymity level of the proxy.
             - `https` (bool): Whether the proxy supports HTTPS.
             - `source` (str): Webpage where proxy was found.

    :rtype: list of dict
    """
    logger.set_message(
        level="INFO",
        message_level="SECTION",
        message="Start proxies scraper",
    )

    # Configure port adapters
    freeProxyList_adapter = FreeProxyList()
    geonode_adapter = Geonode()

    # Create service with each adapter:
    freeProxyList_service = ProxyScraper(freeProxyList_adapter)
    geonode_service = ProxyScraper(geonode_adapter)

    # Process proxies from different sources:
    processed_proxies = []
    processed_proxies += freeProxyList_service.get_proxies(
        country_codes_filter,
        anonymity_filter,
        https_filter,
    )
    processed_proxies += geonode_service.get_proxies(
        country_codes_filter,
        anonymity_filter,
        https_filter,
    )

    logger.set_message(
        level="INFO",
        message_level="SECTION",
        message="Finish proxies scraper",
    )

    logger.set_message(
        level="INFO",
        message=f"Number of proxies scraped: {len(processed_proxies)}",
    )

    return processed_proxies


if __name__ == "__main__":
    result = get_proxies()
    print(result)
