import xmltodict
import requests
import logger
import config

from datetime import datetime, timedelta


def parse_xml_to_dict(xml_input):
    try:
        return xmltodict.parse(xml_input)
    except xmltodict.expat.ExpatError as e:
        logger.error("error: %s", e)


def send_kakao_message(message):
    data = config.send_kakao_message_data
    data['template_object']['text'] = message

    try:
        response = requests.post(config.SEND_KAKAO_MESSAGE_URL, headers=config.kakao_headers, data=data)

        if response.json().get("result_code") == 0:
            print("메시지를 성공적으로 보냈습니다.")
        else:
            print("메시지를 보내지 못했습니다. 오류메시지 : " + str(response.json()))
    except requests.exceptions.RequestException as e:
        logger.error("error: %s", e)


if __name__ == "__main__":

    request_date = datetime.now() - timedelta(days=1)

    params = {
        'serviceKey': config.COVID19_SERVICE_KEY,
        'startCreateDt': request_date.strftime("%Y%m%d"),
        'endCreateDt': request_date.strftime("%Y%m%d")
    }

    try:
        response = requests.get(config.COVID19_URL, params=params)

        if response.ok:
            result = parse_xml_to_dict(response.content)["response"]
            if result['header']['resultCode'] == "00":
                send_kakao_message("확진자 수 :" + result['body']['items']['item']['decideCnt'])
            else:
                send_kakao_message(result['header']['resultMsg'])
    except requests.exceptions.RequestException as e:
        logger.error("error: %s", e)




