# flake8: noqa

# Project imports
from proxies_scraper.adapters.ports.proxies_source import Proxies


# TODO:
class FreeProxyList(Proxies):
    URLS = [
        "http://free-proxy.cz/es/proxylist/country/all/http/date/all",
        "http://free-proxy.cz/es/proxylist/country/all/https/date/all",
    ]
    TABLE_INDEXES = {
        0: "IP_Address",
        1: "Port",
        2: "Protocol",
        3: "Country",
        4: "Region",
        5: "City",
        6: "Anonymity",
        7: "Speed",
        8: "Availability",
        9: "Response",
        10: "Last_Checked",
    }

    def _get_page_proxies(self, driver, proxies_df, max_size):
        # Find proxies IPs:
        self._close_popup(driver)
        driver.find_element("xpath", "//span[@id='clickexport']").click()

        element = driver.find_element("xpath", "//div[@id='zkzk']")
        proxies_ips = element.text.split("\n")

        # Iterate over proxies table:
        table_element = driver.find_element("xpath", "//table[@id='proxy_list']").find_element(By.TAG_NAME, "tbody")
        table_rows_elements = table_element.find_elements(By.TAG_NAME, "tr")

        iteration = 0
        for table_rows_element in table_rows_elements:
            row_cells_elements = table_rows_element.find_elements(By.TAG_NAME, "td")
            if len(row_cells_elements) == 11:
                proxy_model = Common.PROXY_MODEL.copy()

                for index_cell, row_cells_element in enumerate(row_cells_elements):
                    if index_cell == 0:
                        proxy_model[self._proxy_table_indexes[index_cell]] = proxies_ips[iteration]
                    else:
                        proxy_model[self._proxy_table_indexes[index_cell]] = row_cells_element.text
                proxy_model["proxy"] = proxy_model["IP_Address"] + ":" + proxy_model["Port"]
                proxy_model["created_date"] = datetime.now(TIMEZONE_MADRID)
                proxy_model["Anonymity"] = Common.type_converter(proxy_model["Anonymity"], parameter_type="Anonymity")
                proxy_model["Https"] = Common.type_converter(proxy_model["Protocol"], parameter_type="Protocol")

                # Save data on dataframe
                proxy_model_df = pd.DataFrame([proxy_model])
                proxies_df = pd.concat([proxies_df, proxy_model_df], ignore_index=True)

                # Check iteration number:
                iteration += 1
                if iteration == max_size:
                    break

    def _close_popup(self, driver):
        try:
            driver.find_element("xpath", "//*[text()='Close']").click()
        except:
            pass

    def get_proxies(self) -> list:
        # Driver configuration:
        options = Options()
        options.headless = False
        chrome_driver_manager = ChromeDriverManager()
        driver = webdriver.Chrome(chrome_driver_manager.install(), options=options)

        # Iterate over URLs and pages and read proxies:
        for url in self.urls:
            driver.get(url)

            # Get pages:
            paginator_elements = driver.find_element("xpath", "//div[@class='paginator']").find_elements(
                By.TAG_NAME, "a"
            )[:-1]

            # Iterate over each page:
            for paginator_element in paginator_elements:
                proxies_df = self._get_page_proxies(driver, proxies_df, max_size)

                # Go to next page:
                self._close_popup(driver)
                paginator_element.click()

        return proxies_df


if __name__ == "__main__":
    proxy_api_obj = FreeProxyListPage()
    result = proxy_api_obj.get_proxies()
    print(result)
