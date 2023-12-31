from libs.reqParser import get_api_params
from libs.pages.apiPage import PageApi


def pytest_generate_tests(metafunc):
    if metafunc.config.getoption("site"):
        site = metafunc.config.getoption("site")
    else:
        site = 'https://reqres.in'
    print(site)
    result = get_api_params(site)
    metafunc.parametrize("number, site, method, locator", result)
    metafunc.parametrize("setup_driver", [{
    }], indirect=True)


def test_uiApi(setup_driver, number, site,method ,locator):
    api = PageApi(setup_driver)
    try:
        api.getPage(site)
    except:
        pass
    try:
        api.findOutput(number=number,xpath={"tag": "div", "class":"output"},buttonlocator=locator)
    except:
        raise "Не удалось получить данные"
    try:
        request_json,response_json,request_code,response_code = api.checkApiResult(method, site)
    except:
        raise "не получилось получить результат"

    assert request_json == response_json  and  request_code == response_code , "Данные не соответствуют"
