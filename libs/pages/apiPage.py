import requests
from libs.pages.page import Page
import json

class Api:
    grandad = None

    request = None
    outputRequest = None
    requestResult = None

    response = None
    outputResponse = None
    responseResult = None

    _request_ = {"class": ["url"]}
    _outputRequest_ = {"data-key": ["output-request"]}

    _response_ = {"class": ["response-code", "response-code bad"]}
    _outputResponse_ = {"data-key": ["output-response"]}
class PageApi(Page):

    def findOutput(self, number, xpath=None, buttonlocator=None):
        self.api = Api()
        xpath = self.__data2xpath__(xpath)

        try:
            elem = self.findElements(buttonlocator)[number]
        except Exception as e:
            raise f"не удалось найти элемент {e}"
        try:
            elem.click()
            self.sleep(2)
        except Exception as e:
            raise f"Не удалось нажать на элемент {e}"

        if xpath is not None:
            self.api.granddad = self.findElement(xpath)
            print(self.api.granddad)
            args = self.findElements(element=self.api.granddad, xpath=f"({xpath})//*")



        self.api.request = self.selectElement(args, self.api._request_)
        self.api.outputRequest = self.selectElement(args, self.api._outputRequest_)
        self.api.response = self.selectElement(args, self.api._response_)
        self.api.outputResponse = self.selectElement(args, self.api._outputResponse_)
        try:
            self.api.requestResult = json.loads(self.text(self.api.outputRequest))
        except:
            self.api.requestResult = {}
        try:
            self.api.responseResult = json.loads(self.text(self.api.outputResponse))
        except:
            self.api.responseResult = {}

    def checkApiResult(self,method, url):
        try:
            request = requests.request(method,url+self.text(self.api.request),json=self.api.requestResult)
        except:
            raise "Не получилось отправить запрос"
        try:
            request_content = json.loads(request.content)
        except:
            request_content = {}
        print(self.api.responseResult)
        print(request_content)
        if self.api.responseResult == request_content and int(self.api.response.text) == request.status_code:
            return True
        else:
            return False