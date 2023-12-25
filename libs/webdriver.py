from selenium import webdriver
from selenium.webdriver.chrome.service import Service



class WebDriver:
    adaptive = False
    browser = 'Chrome'
    version = 'latest'
    logs = False
    executablePath = "chromedriver"
    driver = None

    def __init__(self, **kwargs):
        """Generate driver

        @param kwargs:
        @param adaptive: default is False
        @param browser: 'Chrome', 'Opera' or 'Firefox'. 'Chrome' is default
        @param version: '0.95'. Latest is default
        """
        for key in kwargs.keys():
            if key == "logs":
                self.logs = kwargs["logs"]
            elif key == "executablePath":
                self.executablePath = kwargs["executablePath"]
            elif key == "browser":
                self.browser = kwargs["browser"]

    def setOptions(self):
        if self.logs:
            self.options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        if self.version != 'latest':
            self.options.set_capability("version", self.version)

    def Chrome(self):
        self.options = webdriver.ChromeOptions()
        self.setOptions()



    def run(self):
        if self.browser == 'Chrome':
            self.Chrome()
            self.driver = webdriver.Chrome(
                service=Service(self.executablePath),
                options=self.options)

    def __del__(self):
        if self.driver is not None:
            self.driver.close()
            self.driver.quit()
