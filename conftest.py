import pytest

from libs.webdriver import WebDriver

def pytest_addoption(parser):
    parser.addoption("--site", type=str, help="Url of site")




@pytest.fixture(scope="function")
def setup_driver(request):
    Driver = WebDriver(logs=True,
                       **request.param)
    Driver.run()
    yield Driver
    del Driver


