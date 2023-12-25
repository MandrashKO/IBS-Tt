import json
from time import sleep, time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Page:
    """
    a class for working with elements on a page
    """
    driver = None
    TIMEOUT = 5  # max time of waiting
    STEPTIME = .5  # repetition period

    def __init__(self, webdriver) -> None:
        """Base class for pages

        :param driver: Selenium WebDriver
        """
        self.webdriver = webdriver
        self.driver = webdriver.driver

    def current_url(self):
        return self.driver.current_url

    def attribute(self, elem, attrib):
        return elem.get_attribute(attrib)

    def attributes(self, elem):
        return self.driver.execute_script('var items = {}; for (index = 0; index < '
                                          'arguments[0].attributes.length; ++index) { '
                                          'items[arguments[0].attributes[index].name] = '
                                          'arguments[0].attributes[index].value }; return '
                                          'items;', elem)

    def __data2xpath__(self, data):
        if type(data) == dict:
            tag = data["tag"] if "tag" in data.keys() else "*"
            attrib = {}
            if "attrib" in data.keys():
                attrib = data["attrib"]
            else:
                for key in data.keys():
                    if key != "tag":
                        attrib[key] = data[key]
        elif type(data) == list:
            tag = ""
            attrib = {}
            for item in data:
                for key in item.keys():
                    if key == "tag":
                        tag = item[key]
                    else:
                        attrib[key] = item[key]
            tag = "*" if tag == "" else tag
        elif type(data) == str:
            return data
        else:
            raise TypeError(f"Не могу преобразовать {data=} типа {type(data)} к xpath")
        atts = ''
        for att in attrib:
            atts = atts + f" and @{att}='{attrib[att]}'"
        atts = '[' + atts[5:] + ']'
        return f"//{tag}{atts}"

    def findElement(self, xpath, element=None):
        xpath = self.__data2xpath__(xpath)
        if element:
            return WebDriverWait(self.driver, self.TIMEOUT, self.STEPTIME).until(
                lambda elem: EC._element_if_visible(element.find_element(By.XPATH, xpath)))
        else:
            return WebDriverWait(self.driver, self.TIMEOUT, self.STEPTIME).until(
                lambda elem: EC._element_if_visible(self.driver.find_element(By.XPATH, xpath)))

    def findElements(self, xpath, element=None):
        xpath = self.__data2xpath__(xpath)
        if element:
            return WebDriverWait(self.driver, self.TIMEOUT, self.STEPTIME).until(
                lambda elems: element.find_elements(By.XPATH, xpath))
        else:
            return WebDriverWait(self.driver, self.TIMEOUT, self.STEPTIME).until(
                lambda elems: (self.driver.find_elements(By.XPATH, xpath)))



    def getPage(self, url, update=True):
        if not update and self.driver.current_url:
            return
        else:
            return self.driver.get(url)

    def sleep(self, time=.05):
        sleep(time)


    def click(self, elem: object = None, xpath: str = None) -> None:
        if elem is None:
            if xpath is not None:
                elem = self.findElement(self.__data2xpath__(xpath))
            else:
                raise Exception("Elem или xpath не должны быть None")
        self.driver.execute_script(f"window.scrollTo(0, {elem.location['y'] - 400})")
        start = time()
        while time() - start < self.TIMEOUT:
            try:
                self.sleep(1)
                elem.click()
                self.sleep(1)
                return True
            except:
                sleep(self.STEPTIME)
        raise TimeoutError(f"Не удалось кликнуть на элемент {self.__data2xpath__(self.attributes(elem))}, {elem}")

    def selectElement(self, elements: list, pattern: dict):
        for arg in elements:
            # print(arg)
            for key in pattern.keys():
                attr = self.attribute(arg, key)
                if attr is not None:
                    if attr.lower() in pattern[key]:
                        try:
                            arg = WebDriverWait(self.driver, self.TIMEOUT, self.STEPTIME).until(
                            lambda elem: EC._element_if_visible(arg))
                        except:
                            arg = None
                        return arg


    def text(self, elem: object = None, xpath: str = None):
        if elem is None:
            if xpath is not None:
                elem = self.findElement(self.__data2xpath__(xpath))
            else:
                raise Exception("Elem или xpath не должны быть None")
        return elem.text

