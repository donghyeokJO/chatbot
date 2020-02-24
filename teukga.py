from flask import Flask, request, jsonify
import requests
import sys
import json
import difflib
from functools import reduce
import random

app = Flask(__name__)

chut = u'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ#'
ga = u'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅢㅢㅣ#'
ggut = u' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄻㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ#'

BASE = 0xAC00


def segment(ch):
    code = ord(ch)-BASE
    jongsung = code % 28

    code = code-jongsung
    jungsung = int((code/28) % 21)

    code = code/28
    chosung = int(code/21)

    if chosung < 0:
        chosung = -1
    if jongsung > 19:
        jongsung = -1

    return chut[chosung], ga[jungsung], ggut[jongsung]


def diff(word1, word2):

    w1 = ''.join(reduce(lambda x1, x2: x1+x2, map(segment, word1)))
    w2 = ''.join(reduce(lambda x1, x2: x1+x2, map(segment, word2)))
    differ = difflib.SequenceMatcher(None, w1, w2)

    return differ.ratio()


best = ['CJ대한통운', '롯데택배', '한진택배', '우체국택배', '로젠택배']
companies = ['CJ대한통운',
             '한진택배',
             '롯데택배',
             '우체국택배',
             '로젠택배',
             '일양로지스',
             'EMS',
             'DHL',
             '한덱스',
             'FedEx',
             'UPS',
             'USPS',
             '대신택배',
             '경동택배',
             '합동택배',
             'CU 편의점택배',
             'CVSnet 편의점택배',
             'TNT Express',
             '한의사랑택배',
             '천일택배',
             '건영택배',
             'GSMNtoN',
             '에어보이익스프레스',
             'KGL네트웍스',
             'DHL Global Mail',
             'i-Parcel',
             '판토스',
             'ECMS Express',
             '굿투럭',
             'GSI Express',
             'CJ대한통운 국제특송',
             '애니트랙',
             '로지스링크(SLX택배)',
             '호남택배',
             '우리한방택배',
             'ACI Express',
             'ACE Express',
             'GPS Logix',
             '성원글로벌카고',
             '세방',
             '농협택배',
             '홈픽택배',
             'EuroParcel',
             'KGB택배',
             'Cway Express',
             '하이택배',
             '지오로직',
             'YJS글로벌(영국)',
             '워펙스코리아',
             '(주)홈이노베이션로지스',
             '은하쉬핑',
             'FLF퍼레버택배',
             'YJS글로벌(월드)',
             'Giant Network Group',
             '디디로지스',
             '우리동네택배',
             '대림통운',
             'LOTOS CORPORATION',
             'IK물류',
             '성훈물류',
             '롯데택배 해외특송']

post_com = {"CJ대한통운": {"web": "www.cjlogistics.com/ko/main", "phone": "1588-1255"},
            "한진택배": {"web": "www.hanjin.co.kr", "phone": "1588-0011"},
            "롯데택배": {"web": "www.lotteglogis.com/home/main", "phone": "1588-2121"},
            "우체국택배": {"web": "www.epost.go.kr", "phone": "1588-1300"},
            "로젠택배": {"web": "www.ilogen.com/web", "phone": "1588-9988"},
            "일양로지스": {"web": "www.ilyanglogis.com/", "phone": "1588-0002"},
            "EMS": {"web": "ems.epost.go.kr/comm.RetrievePostagEMSSrvcCenter.postal", "phone": "1588-1300"},
            "DHL": {"web": "www.logistics.dhl/kr-ko/home.html", "phone": "1588-0001"},
            "한덱스": {"web": "www.e-handex.co.kr/", "phone": "정보 없음"},
            "Fedex": {"web": "www.fedex.com/ko-kr/home.html", "phone": "080-023-8000"},
            "UPS": {"web": "www.ups.com/kr/ko/Home.page", "phone": "1588-6886"},
            "USPS": {"web": "www.usps.com/", "phone": "1-800-275-8777"},
            "대신택배": {"web": "www.ds3211.co.kr/", "phone": "043-222-4582"},
            "경동택배": {"web": "kdexp.com/main.kd", "phone": "1899-5368"},
            "합동택배": {"web": "hdexp.co.kr/index.hd", "phone": "1899-3392"},
            "CU 편의점택배": {"web": "www.cupost.co.kr/postbox/main.cupost", "phone": "1577-1287"},
            "CVSnet 편의점택배": {"web": "www.cvsnet.co.kr/main/index.do", "phone": "1577-1287"},
            "TNT Express": {"web": "www.tnt.com/express/ko_kr/site/home.html", "phone": "1588-0588"},
            "한의사랑택배": {"web": "www.hanips.com/", "phone": "1600-1055"},
            "천일택배": {"web": "www.chunilps.co.kr/kor/main.jsp", "phone": "1877-6606"},
            "건영택배": {"web": "www.kunyoung.com/", "phone": "031-460-2700"},
            "GSMNtoN": {"web": "www.gsmnton.com/gsm/handler/Index", "phone": "1599-6862"},
            "에어보이익스프레스": {"web": "www.airboyexpress.com/", "phone": "070-8269-9906"},
            "KGL네트웍스": {"web": "http://kglnetworks.com/", "phone": "031-944-6182"},
            "DHL Global Mail": {"web": "ems.epost.go.kr/comm.RetrievePostagEMSSrvcCenter.postal", "phone": "1588-1300"},
            "i-Parcel": {"web": "www.i-parcel.com", "phone": "None"},
            "판토스": {"web": "www.pantos.com/kr/main.do", "phone": "02-3771-2114"},
            "ECMS Express": {"web": "ecmsglobal.com/kr/", "phone": "1800-8629"},
            "굿투럭": {"web": "www.goodstoluck.co.kr/", "phone": "1899-9767"},
            "GSI Express": {"web": "www.gsiexpress.com/", "phone": "070-8670-7060"},
            "CJ대한통운 국제특송": {"web": "www.cjlogistics.com/ko/tool/international/tracking", "phone": "1588-1255"},
            "애니트랙": {"web": "www.anytrack.co.kr/", "phone": "02-712-6364"},
            "로지스링크(SLX택배)": {"web": "www.slx.co.kr/", "phone": "1544-6482"},
            "호남택배": {"web": "honamlogis.co.kr/", "phone": "1877-0572"},
            "우리한방택배": {"web": "www.woorihb.com/default/", "phone": "1577-5210"},
            "ACI Express": {"web": "www.aciexpress.net/", "phone": "1588-0300"},
            "ACE Express": {"web": "www.acedp.co.kr/", "phone": "070-4352-2614"},
            "GPS Logix": {"web": "gpslgx.com/", "phone": "310-632-7800"},
            "성원글로벌카고": {"web": "www.swgexp.com/", "phone": "032-746-9984"},
            "세방": {"web": "www.sebang.com/", "phone": "정보 없음"},
            "농협택배": {"web": "ex.nhlogis.co.kr/main.do", "phone": "1588-0011"},
            "홈픽택배": {"web": "homepick.com/", "phone": "1800-0987"},
            "EuroParcel": {"web": "www.duxglobal.co.uk/home/", "phone": "020-7998-1304"},
            "KGB택배": {"web": "www.kgb.co.kr/index.asp", "phone": "02-402-4114"},
            "Cway Express": {"web": "service.cwaycorp.com/tracking?hbl=", "phone": "정보 없음"},
            "하이택배": {"web": "정보 없음", "phone": "정보 없음"},
            "지오로직": {"web": "정보 없음", "phone": "정보 없음"},
            "YJS글로벌(월드)": {"web": "www.yjsglob.com/", "phone": "+82-10-4760-3693"},
            "Giant Network Group": {"web": "www.giantnetworkgroup.com/", "phone": "1588-7457"},
            "디디로지스": {"web": "정보 없음", "phone": "정보 없음"},
            "우리동네택배": {"web": "정보 없음", "phone": "정보 없음"},
            "대림통운": {"web": "daelim2005.modoo.at/", "phone": "053-253-7744"},
            "LOTOS CORPORATION": {"web": "www.lotos.co.jp/WebHome/main.asp", "phone": "+81-3-6278-9408"},
            "IK물류": {"web": "ik82.modoo.at/", "phone": "031-544-4108"},
            "성훈물류": {"web": "www.shfly.co.kr/", "phone": " 043-731-8295"},
            "롯데택배 해외특송": {"web": "www.lotteglogis.com/mobile/business/globallogis/international/express", "phone": "1588-2121"}
            }


@app.route("/ask_post", methods=["POST"])
def ask_post():
    req = request.get_json()
    print(req, file=sys.stderr)
    company = req["action"]["detailParams"]["company"]["value"]
    if company == '홈으로' or company == '홈':
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {

                            "description": "비교할수록 특가스러운 '특가닷컴' 입니다. \n택배배송조회 서비스를 이용하시려면 아래 '택배배송 조회하기' 버튼을 클릭해주세요",
                            "thumnails": {
                                "imageUrl": "http://www.startdoctor.net/tteukga.jpg"
                            },
                            "buttons": [{
                                "action": "block",
                                "label": "택배배송 조회하기",
                                "blockId": "5dd622a2b617ea0001b5d6ba"
                            }
                            ]
                        }
                    }
                ]
            }
        }
        return res
    elif company == '택배배송 조회하기' or company == '배송조회':
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                            "description": "비교할수록 특가스러운 '특가닷컴' 입니다. \n택배배송조회 서비스를 이용하시려면 아래 '택배배송 조회하기' 버튼을 클릭해주세요",
                            "thumnail": {
                                "imageUrl": "https://www.startdoctor.net/tteukga.jpg"
                            },
                            "buttons": [{
                                "action": "block",
                                "label": "택배배송 조회하기",
                                "blockId": "5dd622a2b617ea0001b5d6ba"
                            }
                            ]
                        }
                    }
                ]
            }
        }
        return res
    elif company == '특가닷컴 제휴문의' or company == '제휴문의':
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "365일 특가스러운 쇼핑 특가닷컴에서는 입점 제휴사를 기다리고 있습니다. \n\n상담문의: 4666-3555"

                        }
                    }
                ]
            }
        }
        return res

    elif company == '택배':

        highest = random.choice(best)
    elif "CJ" in company or "cj" in company:
        highest = "CJ대한통운"
    elif "cu" in company or "CU" in company:
        highest = "CU 편의점택배"
    elif "일양" in company:
        highest = "일양로지스"
    else:
        if company in companies:
            highest = company
        elif company.upper() in companies:
            highest = company.upper()
        elif company.lower() in companies:
            highest = company.lower()
        else:
            max = 0
            highest = company
            for com in companies:
                if(diff(company, com) > max):
                    max = diff(company, com)
                    highest = com
    print(highest)
    answer = "입력하신 회사가 '" + highest + \
        "' 가 맞으신가요? \n 맞으시다면 '운송장 번호 입력하기' 버튼을, 그렇지 않다면 '다시 입력하기' 버튼을 눌러주세요. "
    key = "Wielkc7ufKJQC1kB7Nf4jg"
    url = "http://info.sweettracker.co.kr/api/v1/companylist?t_key="+key
    r = requests.get(url, params=None).json()

    company_code = 0
    for i in r['Company']:
        if(i['Name'] == highest):
            company_code = i['Code']

    if company_code == 0:
        answer = "지원하지 않는 택배회사입니다. 택배회사 이름을 정확히 입력해 주세요. \n 정확히 입력하시려면 아래 '다시 입력하기 버튼'을 눌러주세요 \n 입력이 어려우시면 아래 '홈으로' 버튼을 누르세요."
        res = {
            "version": "2.0",

            "template": {
                "outputs": [
                    {
                        "basicCard": {
                            "description": answer,
                            "buttons": [{
                                "action": "block",
                                "label": "다시입력하기",
                                "blockId": "5dd622a2b617ea0001b5d6ba"
                            }, {
                                "action": "block",
                                "label": "홈으로",
                                "blockId": "5ddfb9f4ffa7480001986d82"
                            }
                            ]
                        }
                    }
                ]
            }
        }
        return res
    goid = "5dd622d992690d000194eb92"
    if highest == "한진택배":
        goid = '5dd622d992690d000194eb92'
    elif highest == "롯데택배":
        goid = '5de5f1f0b617ea0001cb1ac4'
    elif highest == "CJ대한통운":
        goid = '5de5f439b617ea0001cb1afe'
    elif highest == "로젠택배":
        goid = '5de5f4bf8192ac0001d6734a'
    elif highest == "우체국택배":
        goid = '5de5f51a8192ac0001d6734e'
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "description": answer,
                        "buttons": [
                            {
                                "action": "block",
                                "label": "운송장 번호 입력하기",
                                "blockId": goid
                            }, {
                                "action": "block",
                                "label": "다시입력하기",
                                "blockId": "5dd622a2b617ea0001b5d6ba"
                            }
                        ]
                    }
                }
            ]
        }
    }
    return jsonify(res)


@app.route("/ask_number", methods=["POST"])
def ask_number():
    req = request.get_json()
    print(req, file=sys.stderr)
    code = req["action"]["detailParams"]["code"]["value"]
    company = req['action']['detailParams']['company']["value"]
    # company = '한진택배'

    if code == '홈으로' or code == '홈':
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                            "thumnail": {
                                "imageUrl": "https://www.startdoctor.net/tteukga.jpg"
                            },
                            "description": "비교할수록 특가스러운 '특가닷컴' 입니다. \n택배배송조회 서비스를 이용하시려면 아래 '택배배송 조회하기' 버튼을 클릭해주세요",
                            "buttons": [{
                                "action": "block",
                                "label": "택배배송 조회하기",
                                "blockId": "5dd622a2b617ea0001b5d6ba"
                            }
                            ]
                        }
                    }
                ]
            }
        }
        return res
    elif company in companies:
        highest = company
    elif "CJ" in company or "cj" in company:
        highest = "CJ대한통운"
    elif "cu" in company or "CU" in company:
        highest = "CU 편의점택배"
    elif "일양" in company:
        highest = "일양로지스"
    else:
        if company in companies:
            highest = company
        elif company.upper() in companies:
            highest = company.upper()
        elif company.lower() in companies:
            highest = company.lower()
        else:
            max = 0
            highest = company
            for com in companies:
                if(diff(company, com) > max):
                    max = diff(company, com)
                    highest = com

    key = "Wielkc7ufKJQC1kB7Nf4jg"
    url = "http://info.sweettracker.co.kr/api/v1/companylist?t_key="+key
    r = requests.get(url, params=None).json()
    company_code = 0
    for i in r['Company']:
        if(i['Name'] == highest):
            company_code = i['Code']

    if company_code == 0:
        answer = "잘못된 택배회사 입력입니다."
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                            "description": answer,
                            "buttons": [{
                                "action": "block",
                                "label": "다시 입력하기",
                                "blockId": "5dd622a2b617ea0001b5d6ba"
                            }
                            ]
                        }
                    }
                ]
            }
        }
        return res
    url = "http://info.sweettracker.co.kr/api/v1/trackingInfo?t_key=" + \
        key+"&t_code="+company_code+"&t_invoice="+code

    r = requests.get(url, params=None).json()
    if 'status' in r:
        if(r['status'] == False):
            answer = '유효하지 않은 운송장 번호입니다.' + '\n' + \
                '처음부터 다시 정확하게 입력해주세요. \n입력이 어려우시면 아래 "홈으로" 버튼을 클릭해주세요.'
            answer = answer + '\n' + highest + " 전화번호 : " + \
                post_com[highest]['phone'] + '\n' + \
                "웹 사이트 주소 : " + post_com[highest]['web']
            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "description": answer,
                                "buttons": [{
                                    "action": "block",
                                    "label": "다시 입력하기",
                                    "blockId": "5dd622a2b617ea0001b5d6ba"
                                }, {
                                    "action": "block",
                                    "label": "홈으로",
                                    "blockId": "5ddfb9f4ffa7480001986d82"
                                }
                                ]
                            }
                        }
                    ]
                }
            }
            return jsonify(res)
    elif r['level'] == 1:
        answer = "운송장이 등록되지 않았거나 업체에서 상품 준비중입니다."
        answer = answer + '\n' + highest + " 전화번호 : " + \
            post_com[highest]['phone'] + '\n' + \
            "웹 사이트 주소 : " + post_com[highest]['web']
    else:
        answer = '보내는 사람 : ' + r['senderName'] + '\n' + '받는 사람 : ' + \
            r['receiverName'] + '\n' + '제품정보 : ' + r['itemName'] + '\n'
        answer += '현재 위치 : ' + \
            r['trackingDetails'][-1]['where'] + '\n배송상태 : ' + \
            r['trackingDetails'][-1]['kind'] + \
            '\n담당자 연락처 : ' + r['trackingDetails'][-1]['telno2']
        answer = answer + '\n' + highest + " 전화번호 : " + \
            post_com[highest]['phone'] + '\n' + \
            "웹 사이트 주소 : " + post_com[highest]['web']
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                   {
                       "basicCard": {
                           "description": answer,
                           "buttons": [{
                               "action": "block",
                               "label": "배송조회 더 하기",
                               "blockId": "5dd622a2b617ea0001b5d6ba"
                           }, {
                               "action": "block",
                               "label": "홈으로",
                               "blockId": "5ddfb9f4ffa7480001986d82"
                           }
                           ]
                       }
                   }
            ]
        }
    }
    return jsonify(res)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug="on", port="8000")
