
from bs4 import BeautifulSoup
import requests
from lxml import etree


def get_api_params(site):
    locator = '//li[@data-http]'
    response = requests.get(site)
    html = BeautifulSoup(response.content, "html.parser")
    exp = etree.HTML(str(html)).xpath(locator)
    return [(number,site,method.attrib["data-http"], locator) for number, method in enumerate(exp)]
