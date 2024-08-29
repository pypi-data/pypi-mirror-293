from proxies_scraper.adapters.ports.proxies_source import Proxies
from proxies_scraper.utils.file_operation import FileOperations
from proxies_scraper.utils.logger import Logger


class ProxyScraper:
    def __init__(self, proxy_port: Proxies):
        self.proxy_port = proxy_port

        # Set logger:
        self._logger = Logger(
            module=FileOperations.get_file_name(__file__, False),
            level="INFO",
        )  # Set in configuration file

    def _get_page_proxies(self):
        proxies = []
        try:
            proxies = self.proxy_port.get_proxies()
        except Exception as e:
            self._logger.set_message(
                level="WARNING",
                message_level="MESSAGE",
                message=f"Proxies page {self.proxy_port.NAME!s} scraping failed due to the "
                f"following exception {e!s}",
            )
        return proxies

    @staticmethod
    def _filter_proxies(
        proxies: list,
        country_codes_filter: list | None,
        anonymity_filter: list | None,
        https_filter: bool | None,
    ):
        if isinstance(country_codes_filter, list):
            proxies = [proxy for proxy in proxies if proxy["country_code"] in country_codes_filter]
        if isinstance(anonymity_filter, list):
            proxies = [proxy for proxy in proxies if proxy["anonymity"] in anonymity_filter]
        if isinstance(https_filter, bool):
            proxies = [proxy for proxy in proxies if proxy["https"] == https_filter]
        return proxies

    def get_proxies(
        self,
        country_codes_filter: list | None = None,
        anonymity_filter: list | None = None,
        https_filter: bool | None = None,
    ):
        self._logger.set_message(
            level="INFO",
            message_level="SUBSECTION",
            message=f"Process proxies from {self.proxy_port.NAME}",
        )

        self._logger.set_message(level="INFO", message="Read proxies")
        proxies = self._get_page_proxies()

        self._logger.set_message(level="INFO", message="Filter proxies")
        proxies = self._filter_proxies(
            proxies,
            country_codes_filter,
            anonymity_filter,
            https_filter,
        )

        return proxies
