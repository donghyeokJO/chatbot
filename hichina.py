from flask import Flask, request, jsonify
import requests
import sys
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

app = Flask(__name__)

start_block_id = '5d9f2e2fb617ea00012b20ad'
GO_FIRST_BTN = {"action": "block",
                "label": "홈으로", "blockId": start_block_id}
GO_TO = {"action": "block",
         "label": "더 검색해보기", "blockId": '5da84424ffa7480001db1807'}


@app.route("/search", methods=['POST'])
def search():
    req = request.get_json()
    code = req["action"]["detailParams"]["sys_text"]["value"]

    if(iskorean(code)):
        answer = "잘못된 상품 코드입니다. 코드 검색은 현재 에픽세븐 npc 업체만 가능한 기능입니다. 더 검색하기를 클릭 후 안내에 따라 코드를 다시 입력해주세요"
    else:
        url = "http://npc233.com/play/index.php/home/index/f_check?id="+code
        html = urlopen(url)

        bs = BeautifulSoup(html, "html.parser")
        link = bs.find_all('td')

        if(len(link) == 0):
            answer = "잘못된 상품 코드입니다. 코드 검색은 현재 에픽세븐 npc 업체만 가능한 기능입니다. 더 검색하기를 클릭 후 안내에 따라 코드를 다시 입력해주세요"
        else:
            yen = link[1].text.strip()
            y = yen[1:5]
            num_yen = float(y)
            won = num_yen*183.75+3000
            won = round(won)
            answer = "수수료 포함 총 " + \
                str(won)+" 원 입니다. 구매를 원하시면 채팅창에 '계좌' 입력 후 나오는 계좌로 입금 부탁드립니다."
    # 아이디 없을 때는 다시 묻기
    res = {"version": "2.0",
           "template": {
               "outputs": [
                   {
                       "basicCard": {
                           "description": answer,
                           "buttons": [GO_TO
                                       ]
                       }
                   }
               ]
           }
           }
    return res


def iskorean(input_s):
    hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', input_s))
    return hanCount > 0


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug="on", port="8000")
