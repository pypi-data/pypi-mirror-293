from bs4 import BeautifulSoup

# Project imports
from proxies_scraper.adapters.ports.proxies_source import Proxies
from proxies_scraper.utils.postman import Postman
from proxies_scraper.utils.time_operations import Time


class FreeProxyList(Proxies):
    NAME = "free-proxy-list.net"
    URL = "https://free-proxy-list.net/"
    TABLE_INDEXES = {
        0: "IP_Address",
        1: "Port",
        2: "Code",
        3: "Country",
        4: "Anonymity",
        5: "Google",
        6: "Https",
        7: "Last_Checked",
    }
    MODEL_MAPPER = {
        "IP_Address": "ip_address",
        "Port": "port",
        "Code": "country_code",
        "Country": "country",
        "Anonymity": "anonymity",
        "Https": "https",
        "Last_Checked": "last_checked",
    }

    def get_proxies(self) -> list:
        proxy_model_list = []

        # Get Free Proxy HTML:
        response = Postman.send_request(
            method="GET",
            url=self.URL,
            status_code_check=200,
        )

        html_doc = BeautifulSoup(response.content, "html.parser")

        # Iterate over proxies table:
        table = (
            html_doc.find("section", id="list")
            .findChildren("table")[0]  # type: ignore
            .findChildren("tbody")[0]
        )
        table_rows = table.findChildren("tr")

        for table_row in table_rows:
            row_cells = table_row.findChildren("td")

            proxy = {}
            for index_cell, row_cell in enumerate(row_cells):
                proxy[self.TABLE_INDEXES[index_cell]] = row_cell.text

            proxy_model = self._dict_mapper(proxy)

            proxy_model["proxy"] = proxy_model["ip_address"] + ":" + proxy_model["port"]
            proxy_model["created_date"] = Time.get_datetime(self.TIMEZONE)
            proxy_model["anonymity"] = self._type_converter(
                proxy_model["anonymity"],
                parameter_type="anonymity",
            )
            proxy_model["https"] = self._type_converter(
                proxy_model["https"],
                parameter_type="affirmation",
            )
            proxy_model["source"] = self.NAME

            proxy_model_list.append(proxy_model)
        return proxy_model_list


if __name__ == "__main__":
    proxy_api_obj = FreeProxyList()
    result = proxy_api_obj.get_proxies()
    print(result)
