from proxies_scraper.adapters.ports.proxies_source import Proxies
from proxies_scraper.utils.postman import Postman
from proxies_scraper.utils.time_operations import Time


class Geonode(Proxies):
    NAME = "proxylist.geonode.com"
    URL = (
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=<page>&sort_by=lastChecked&sort_type=desc"
        "&protocols=http%2Chttps&anonymityLevel=elite&anonymityLevel=anonymous"
    )
    HEADERS = {
        "Host": "proxylist.geonode.com",
        "Accept": "application/json, text/plain",
        "Origin": "https://geonode.com",
        "Referer": "https://geonode.com/",
    }
    MODEL_MAPPER = {
        "ip": "ip_address",
        "port": "port",
        "country": "country_code",
        "anonymityLevel": "anonymity",
        "protocols": "https",
        "lastChecked": "last_checked",
    }

    def _set_url(self, page: int) -> str:
        return self.URL.replace("<page>", str(page))

    def get_proxies(self) -> list:
        proxy_model_list = []

        page = 1
        number_proxies = 500
        while number_proxies != 0:
            # Get Free Proxy HTML:
            url = self._set_url(page=page)
            response = Postman.send_request(
                method="GET",
                url=url,
                headers=self.HEADERS,
                status_code_check=200,
            )
            response_data = response.json()

            # Iterate over proxies:
            number_proxies = len(response_data["data"])
            for proxy in response_data["data"]:
                proxy_model = self._dict_mapper(proxy)

                proxy_model["proxy"] = proxy_model["ip_address"] + ":" + proxy_model["port"]
                proxy_model["created_date"] = Time.get_datetime(self.TIMEZONE)
                proxy_model["anonymity"] = self._type_converter(
                    proxy_model["anonymity"],
                    parameter_type="anonymity",
                )
                proxy_model["https"] = self._type_converter(
                    proxy_model["https"][0],
                    parameter_type="protocol",
                )  # TODO: find element in list
                proxy_model["last_checked"] = proxy_model["last_checked"]
                proxy_model["source"] = self.NAME

                proxy_model_list.append(proxy_model)

            page += 1

        return proxy_model_list


if __name__ == "__main__":
    proxy_api_obj = Geonode()
    result = proxy_api_obj.get_proxies()
    print(result)
