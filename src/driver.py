from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Driver:
    def __init__(self, url):
        self._driver = self._load_chrome()
        self._active = False
        self._url = url

    def _load_chrome(self):
        """ loads a chrome driver """
        options = webdriver.ChromeOptions()

        # using headless mode for better performance
        options.add_argument('--headless')

        return webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), chrome_options=options
        )

    def get(self):
        if not self._active:
            self._driver.get(self._url)
            self._active = True

        return self._driver

    def reload(self):
        self._active = False
        self.get()

    def wait(self, name):
        return WebDriverWait(self.get(), 10).until(
            ec.visibility_of_element_located((By.ID, name))
        )

    def wait_clickable(self, name):
        return WebDriverWait(self.get(), 10).until(
            ec.element_to_be_clickable((By.ID, name))
        )

    def wait_child_by_css(self, selector):
        return WebDriverWait(self.get(), 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )

    def child_by_class(self, parent: WebElement, name):
        return self.children_by_class(parent, name)[0]

    def children_by_class(self, parent: WebElement, name):
        return parent.find_elements(by=By.CLASS_NAME, value=name)

    def children_by_tag(self, parent: WebElement, tag):
        return parent.find_elements(by=By.TAG_NAME, value=tag)
