import sys
import xmltodict
import json

from twisted.python import log
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote_plus
import requests


def send_kakao_message(result):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
       "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "Authorization": "Bearer {Kakao Token}"
    }

    data = {
        "template_object": json.dumps(
            {
                "object_type": "text",
                "text": result["resultMsg"],
                "link": {
                    "web_url": "https://developers.kakao.com",
                    "mobile_web_url": "https://developers.kakao.com"
                },
                "button_title": "바로 확인"
             }
        )
    }

    with requests.post(url, headers=headers, data=data) as response:
        if response.json().get("result_code") == 0:
            print("메시지를 성공적으로 보냈습니다.")
        else:
            print("메시지를 보내지 못했습니다. 오류메시지 : " + str(response.json()))


if __name__ == "__main__":
    log.startLogging(sys.stdout)

    url = "http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson"
    params = "?" + urlencode({
        quote_plus("serviceKey"): "API Token",
        quote_plus("pageNo"): "1",
        quote_plus("numOfRows"): "10",
        quote_plus("startCreateDt"): "20210914",
        quote_plus("endCreateDt"): "20210914"
    })

    request = Request(url + params)
    request.get_method = lambda: "GET"

    try:
        response = urlopen(request).read()
        result = xmltodict.parse(response)["response"]["header"]
        send_kakao_message(result)
    except:
        print("request error")





