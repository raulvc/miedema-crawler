from itertools import combinations

from src.crawler.crawler import Crawler


class PairsCrawler(Crawler):
    def __init__(self, url):
        super().__init__(url)

    def run(self):
        return self._get_pairs()

    def _get_pairs(self):
        self._select_property()
        elems = self._crawl_elems()
        self._driver.reload()  # breaks otherwise

        return list(combinations(elems, 2))

    def _crawl_elems(self):
        """ retrieves available elements """
        content = self._crawl_elem_content("elements-a-combobox")
        elems = self._driver.children_by_tag(content, "div")

        return [i.get_attribute('innerText') for i in elems]

