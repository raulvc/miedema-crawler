from math import floor

from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains

from src.crawler.crawler import Crawler

PIXEL_SPACING = 3  # moves mouse by this much to find value through hover tooltip

# spacing adjustments for special cases:
LEFT_ALIGNED = {
    # label: actual key
    '0.0': '0.01',
    '0.8': '0.8'
}
RIGHT_ALIGNED = {
    # label: actual key
    '1.0': '0.99'
}


class ValuesCrawler(Crawler):

    def __init__(self, url, pair):
        super().__init__(url)
        self._pair = pair

    def run(self):
        self._select_property()
        self._select_elems()
        self._calculate()
        return self._crawl_canvas()

    def _select_elems(self):
        first_elem, second_elem = self._pair
        self._select_elem(combobox_id="elements-a-combobox", elem=first_elem)
        self._select_elem(combobox_id="elements-b-combobox", elem=second_elem)

    def _select_elem(self, combobox_id, elem):
        content = self._crawl_elem_content(combobox_id)
        elem_div = content.find_element(value=elem)
        elem_div.click()

    def _calculate(self):
        calc_button = self._driver.wait_clickable("calculate-button")
        calc_button.click()

    def _crawl_canvas(self):
        container = self._driver.get().find_element(value="main-box")
        canvas = self._driver.child_by_class(container, "overlay")
        canvas.click()

        search_range = self._canvas_search_range(canvas)

        ticks = self._crawl_ticks(container)
        values = {}
        for tick in ticks:
            key, raw_value = self._find_hover(tick, search_range)
            values[key] = self._parse_value(raw_value)

        return values

    def _canvas_search_range(self, canvas):
        canvas_height = canvas.size['height']

        # NOTE: starts 2px above tick label
        return range(2, canvas_height, PIXEL_SPACING)

    def _find_hover(self, tick, search_range):
        tick_key = tick.get_attribute("innerHTML")
        tick_action = ActionChains(self._driver.get())
        tick_action.move_to_element(tick).perform()

        # special cases
        if tick_key in LEFT_ALIGNED.keys():
            self._left_aligned_corner_case()
            tick_key = LEFT_ALIGNED[tick_key]  # for a few cases key isn't the actual value (e.g.: 0.0 -> 0.01)

        if tick_key in RIGHT_ALIGNED.keys():
            self._right_aligned_corner_case()
            tick_key = RIGHT_ALIGNED[tick_key]

        pretty_pair = ''.join(self._pair)  # for logging purposes

        max_range = search_range[-1]
        for i in search_range:
            elem = self._crawl_tooltip()

            if elem:
                value = elem.get_attribute("innerHTML")
                print(f'[{pretty_pair}][{tick_key}] pixel [{i}] tooltip: [{value}]')
                return tick_key, value

            percentage = f"{floor(i / max_range * 100)}%"
            print(f"[{pretty_pair}][{tick_key}][{percentage}] pixel [{i} of {max_range}] ... ")

        raise "couldn't find tick"

    def _left_aligned_corner_case(self):
        # fixes slightly left aligned tick
        align_action = ActionChains(self._driver.get())
        align_action.move_by_offset(6, 0).perform()

    def _right_aligned_corner_case(self):
        # fixes slightly right aligned tick
        align_action = ActionChains(self._driver.get())
        align_action.move_by_offset(-6, 0).perform()

    def _crawl_tooltip(self):
        tooltip_action = ActionChains(self._driver.get())
        tooltip_action.move_by_offset(0, -PIXEL_SPACING).perform()

        try:
            return self._driver.get().find_element(value="tooltip")
        except NoSuchElementException:
            return None

    def _crawl_ticks(self, container):
        x_axis = self._driver.child_by_class(container, "xAxis")
        return self._driver.children_by_tag(x_axis, "div")

    def _parse_value(self, raw_value):
        last_part = raw_value.split(",")[-1]
        return ''.join(c for c in last_part if self._is_number_part(c))

    def _is_number_part(self, c):
        if c.isdigit() or c == '-' or c == '.':
            return True
        return False
