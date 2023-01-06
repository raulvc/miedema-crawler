from src.driver import Driver


class Crawler:
    """ abstract base class for crawlers """

    def __init__(self, url):
        self._driver = Driver(url)

    def _select_property(self):
        """ sets mixing property before proceeding """
        prop_control = self._driver.wait("property-combobox_input")
        prop_control.click()

        mixing_div = self._driver.wait("enthalpy of mixing")
        mixing_div.click()

    def _crawl_elem_content(self, combobox_id):
        combobox = self._driver.get().find_element(value=combobox_id)
        combobox.click()

        container_name = f"{combobox_id}_ctr"
        container = self._driver.wait(container_name)

        return self._driver.child_by_class(container, "content")
