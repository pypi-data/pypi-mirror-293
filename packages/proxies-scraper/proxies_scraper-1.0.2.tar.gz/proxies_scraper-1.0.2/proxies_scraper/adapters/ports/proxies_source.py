import enum

from proxies_scraper.utils.postman import Postman


class Anonymity(enum.Enum):
    ELITE = 1
    ANONYMOUS = 2
    TRANSPARENT = 3


class Proxies:
    NAME = ""
    URL = ""
    HEADERS: dict[str, str] = {}
    MODEL = {
        "ip_address": None,
        "port": None,
        "proxy": None,
        "country_code": None,
        "country": None,
        "anonymity": None,
        "https": None,
        # "available": None, # TODO
        "source": None,
    }
    MODEL_MAPPER: dict[str, str] = {}
    TIMEZONE = "Europe/Madrid"

    @staticmethod
    def _type_converter(value, parameter_type):
        if parameter_type == "affirmation":
            if value == "yes":
                return True
            if value == "no":
                return False
            return False

        if parameter_type == "protocol":
            return bool(value == "HTTPS" or value == "https")

        if parameter_type == "anonymity":
            if value == "elite proxy" or value == "elite" or value == "Alto anonimato" or value == "Elite":
                return Anonymity.ELITE.value
            if value == "transparent" or value == "Transparente":
                return Anonymity.TRANSPARENT.value
            if value == "anonymous" or value == "Anónimo":
                return Anonymity.ANONYMOUS.value
            return None

        raise Exception(f"Unknown parameter type conversion: {parameter_type}")

    def _api_request(self, url=None) -> dict:
        try:
            response = Postman.send_request(
                method="GET",
                url=self.URL if url is None else url,
                headers=self.HEADERS,
                status_code_check=200,
            )
        except Exception as exc:
            print(f"Api request failed: {exc!s}")
            response = {}
        return response

    def _dict_mapper(self, unmapped_dict) -> dict:
        mapped_dict = self.MODEL.copy()
        for key, value in unmapped_dict.items():
            if key in self.MODEL_MAPPER:
                mapped_dict[self.MODEL_MAPPER[key]] = value
        return mapped_dict

    def _model_validator(self, data_dict) -> dict:
        for key in data_dict:
            if key not in self.MODEL:
                raise Exception(
                    f"Data dictionary {data_dict} has incorrect model key: {key}",
                )
        return data_dict

    def get_proxies(self) -> list:
        return []
