from flask import Flask, request, jsonify, session, make_response


import sys
import pymysql
import requests


def database():
    db = pymysql.connect(host="eszett-database.cwxq9xvnodtq.ap-northeast-2.rds.amazonaws.com", user="root", password="medi180615", db="eszett_web", charset="utf8", autocommit=True,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()

    return cursor


start_block_id = '5d886cd88192ac00010c8fa2'
back_point_id = '5d92f59dffa7480001da96d6'
write_block_id = '5d8daa0392690d00016899b6'

ERROR_MESSAGE = '네트워크 접속에 문제가 발생하였습니다. 잠시 후 다시 시도해주세요.'
GO_FIRST_BTN = {"action": "block", "label": "홈으로", "blockId": start_block_id}
GO_LOGIN_BTN = {"action": "block", "label": "로그인하기",
                "blockId": "5d8d9a1cb617ea000180ac3e"}
FIRST_BTN = {"action": "block", "label": "홈으로", "blockId": back_point_id}

app = Flask(__name__)


@app.route('/keyword', methods=['POST'])
def keyword():
    sql2 = "select * from eszett_web.auth_user"
    cursor = database()
    cursor.execute(sql2)

    row = cursor.fetchall()

    req = request.get_json()
    print(req, file=sys.stderr)
    u_id = req['userRequest']['user']['id']

    for ret in row:
        if u_id == ret['kakao_id']:
            if ret['verify'] == 1:
                break
            else:
                res = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "basicCard": {
                                    "title": "유료 회원권을 구매하신 분들만 이용하실 수 있습니다.",
                                    "buttons": [{
                                        "action": "webLink",
                                        "label": "유료 이용권 구매하기",
                                        "webLinkUrl": "https://www.startdoctor.net/mypage/change_pay.php",
                                    }]
                                }
                            }
                        ]
                    }
                }
                return jsonify(res)
        else:
            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": "로그인 세션이 만료되었습니다. 다시 로그인해주세요",
                                "buttons": [GO_LOGIN_BTN]
                            }
                        }
                    ]
                }
            }

        return res

    block_id = req['userRequest']['block']['id']
    subject = req['action']['detailParams']['subject']['value']
    subject_res = requests.post(
        'http://commercial-env.apkxyagrzb.ap-northeast-2.elasticbeanstalk.com/bot/keyword/', data={'subject': subject}).json()
    str1 = "/".join(str(e) for e in subject_res['키워드'])
    str2 = "/".join(str(e) for e in subject_res['월간PC검색'])
    str3 = "/".join(str(e) for e in subject_res['월간모바일검색'])
    str4 = "/".join(str(e) for e in subject_res['월평균PC클릭'])
    str5 = "/".join(str(e) for e in subject_res['월평균모바일클릭'])
    str6 = "/".join(str(e) for e in subject_res['월평균PC클릭률'])
    str7 = "/".join(str(e) for e in subject_res['월평균모바일클릭률'])
    str8 = "/".join(str(e) for e in subject_res['경쟁정도'])
    str9 = "/".join(str(e) for e in subject_res['월평균노출광고수'])
    answer = "키워드 : " + str1 + "\n\n" + "월간 PC검색: " + str2 + "\n\n" + "월간 모바일 검색: " + str3 + "\n\n" + "월평균PC클릭: " + str4 + "\n\n"+"월평균 모바일 클릭: " + \
        str5 + "\n\n"+"월평균 PC클릭률: " + str6+"\n\n"+"월평균 모바일 클릭률: " +  \
        str7 + "\n\n" + "경쟁정도: " + str8 + "\n\n"+"월 평균 노출 광고수: " + str9
    res = {

        "version": "2.0",
        "template": {
            "outputs": [
                    {
                        "simpleText": {
                            "text": answer
                        }
                    }
            ]
        }
    }
    return jsonify(res)


@app.route('/keyword_one', methods=['POST'])
def keyword_one():

    sql2 = "select * from eszett_web.auth_user"
    cursor = database()

    cursor.execute(sql2)

    row = cursor.fetchall()

    req = request.get_json()
    print(req, file=sys.stderr)
    u_id = req['userRequest']['user']['id']
    print(u_id)
    for ret in row:
        if u_id == ret['kakao_id']:
            if ret['verify'] == 1:
                break
            else:
                res = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "basicCard": {
                                    "title": "유료 회원권을 구매하신 분들만 이용하실 수 있습니다.",
                                    "buttons": [{
                                        "action": "webLink",
                                        "label": "유료 이용권 구매하기",
                                        "webLinkUrl": "https://www.startdoctor.net/mypage/change_pay.php",
                                    }]
                                }
                            }
                        ]
                    }
                }
                return jsonify(res)
        else:
            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": "로그인 세션이 만료되었습니다. 다시 로그인해주세요",
                                "buttons": [GO_LOGIN_BTN]
                            }
                        }
                    ]
                }
            }

        return res

    block_id = req['userRequest']['block']['id']
    subject = req['action']['detailParams']['subject']['value']
    subject_res = requests.post(
        'http://commercial-env.apkxyagrzb.ap-northeast-2.elasticbeanstalk.com/bot/keyword_one/', data={'subject': subject}).json()
    str1 = "/".join(str(e) for e in subject_res['키워드'])
    str2 = "/".join(str(e) for e in subject_res['월간PC검색'])
    str3 = "/".join(str(e) for e in subject_res['월간모바일검색'])
    str4 = "/".join(str(e) for e in subject_res['월평균PC클릭'])
    str5 = "/".join(str(e) for e in subject_res['월평균모바일클릭'])
    str6 = "/".join(str(e) for e in subject_res['월평균PC클릭률'])
    str7 = "/".join(str(e) for e in subject_res['월평균모바일클릭률'])
    str8 = "/".join(str(e) for e in subject_res['경쟁정도'])
    str9 = "/".join(str(e) for e in subject_res['월평균노출광고수'])
    answer = "키워드 : " + str1 + "\n\n" + "월간 PC검색: " + str2 + "\n\n" + "월간 모바일 검색: " + str3 + "\n\n" + "월평균PC클릭: " + str4 + "\n\n"+"월평균 모바일 클릭: " + \
        str5 + "\n\n"+"월평균 PC클릭률: " + str6+"\n\n"+"월평균 모바일 클릭률: " +  \
        str7 + "\n\n" + "경쟁정도: " + str8 + "\n\n"+"월 평균 노출 광고수: " + str9
    res = {

        "version": "2.0",
        "template": {
            "outputs": [
                    {
                        "simpleText": {
                            "text": answer
                        }
                    }
            ]
        }
    }
    return jsonify(res)


@app.route('/login', methods=['POST'])
def login():
    cursor = database()
    sql = "select * from eszett_web.user"

    cursor.execute(sql)

    result = cursor.fetchall()

    req = request.get_json()
    print(req, file=sys.stderr)

    block_id = req['userRequest']['block']['id']
    u_id = req['userRequest']['user']['id']
    print(u_id)
    user_id = req["action"]["detailParams"]["sys_text"]["value"]
    if user_id == '개원상권분석':
        res = {"version": "2.0",
               "template": {
                   "outputs": [
                       {
                           "basicCard": {

                               "description": "개원상권분석이란?\n\n스타트닥터만의 차별화된 빅데이터 기술로 희망하는 개원 장소의 입지를 분석해드리는 서비스입니다.\n\n내게 맞는 개원 자리,\n스타트닥터 개원상권분석 시스템으로 확인해보세요",
                               "buttons": [
                                   {"action": "webLink", "label": "내게 맞는 상권 보러가기",
                                    "webLinkUrl": "http://startdoctor.net/company/system.php"}
                               ]
                           }
                       }
                   ]
               }
               }
        return res
    elif user_id == '홈페이지 바로가기':
        res = {"version": "2.0",
               "template": {
                   "outputs": [
                       {
                           "basicCard": {

                               "description": "스타트 닥터 홈페이지로 이동하시려면 아래 버튼을 클릭해주세요",
                               "buttons": [
                                   {"action": "webLink", "label": "홈페이지 바로가기",
                                    "webLinkUrl": "http://startdoctor.net"}
                               ]
                           }
                       }
                   ]
               }
               }
        return res
    elif user_id == '키워드 검색':
        res = {"version": "2.0",
               "template": {
                   "outputs": [
                       {
                           "basicCard": {

                               "description": "키워드 검색을 이용하시려면 아래 버튼을 클릭해주세요",
                               "buttons": [
                                   {"action": "block", "label": "키워드 검색하기",
                                    "blockId": "5dd215ecb617ea0001b5a6c0"}
                               ]
                           }
                       }
                   ]
               }
               }
        return res
    elif user_id == '키워드 추천':
        res = {"version": "2.0",
               "template": {
                   "outputs": [
                       {
                           "basicCard": {

                               "description": "키워드 추천을 이용하시려면 아래 버튼을 클릭해주세요",
                               "buttons": [
                                   {"action": "block", "label": "키워드 추천받기",
                                    "blockId": "5dd0fa3b8192ac000119e1a6"}
                               ]
                           }
                       }
                   ]
               }
               }
        return res
    elif user_id == '상담채팅':
        res = {"version": "2.0",
               "template": {
                   "outputs": [
                       {
                           "basicCard": {

                               "description": "상담채팅이란?\n의사들이 직접 평가하고 엄선하여 신뢰성 있는 다양한 분야의 업체들과의 채팅 서비스입니다.\n\n궁금하신 내용,\n상담채팅으로 지금 바로 해결해보세요.",
                               "buttons": [
                                   {"action": "webLink", "label": "상담채팅 바로가기",
                                    "webLinkUrl": "http://startdoctor.net/service/chat.php"}
                               ]
                           }
                       }
                   ]
               }
               }
        return res
    elif user_id == '비교견적':
        res = {"version": "2.0",
               "template": {
                   "outputs": [
                       {
                           "basicCard": {

                               "description": "비교견적이란?\n한 번의 문의로 선별된 업체들의 견적서를 받고 비교해볼 수 있는 서비스입니다.\n\n원하시는 종류의 서비스를 선택하신 후,설문을 작성해주시면 신청이 완료됩니다.",
                               "buttons": [
                                   {"action": "webLink", "label": "비교견적 바로가기",
                                    "webLinkUrl": "http://startdoctor.net/service/estimate.php"}
                               ]
                           }
                       }
                   ]
               }
               }
        return res

    user_id = int(user_id)

    for row in result:
        test_id = row['u_license']
        if(row['u_count']) == 0:
            yes = 0
        else:
            yes = 1
        if user_id == test_id:
            answer = row['u_name']+"님" + " 확인 되었습니다."
            query = "insert into auth_user(kakao_id,u_id,verify) values(%s,%s,%s)"
            cursor.execute(query, (u_id, row['u_id'], yes))

            # 아이디 없을 때는 다시 묻기
            res = {"version": "2.0",
                   "template": {
                       "outputs": [
                           {
                              "basicCard": {
                                  "title": answer,
                                  "buttons": [
                                      FIRST_BTN
                                  ]
                              }
                           }
                       ]
                   }
                   }
            break

        else:
            answer = "회원가입 되지 않은 면허번호입니다. 사이트로 이동해서 회원 가입을 진행해주세요."
            # 아이디 없을 때는 다시 묻기
            res = {"version": "2.0",
                   "template": {
                       "outputs": [
                           {
                               "basicCard": {
                                   "title": answer,
                                   "buttons": [{
                                       "action": "block",
                                       "label": "다시 입력",
                                       "blockId": block_id
                                   }, {
                                       "action": "webLink",
                                       "label": "회원가입하기",
                                       "webLinkUrl": "https://www.startdoctor.net",
                                   }, GO_FIRST_BTN]
                               }
                           }
                       ]
                   }
                   }

    return jsonify(res)


# @app.route('/f1_1', methods=['POST'])
# def f1_1():
#     req = request.get_json()
#     print(req, file=sys.stderr)
#     # print(session['u_id'])

#     sql2 = "select * from eszett_web.auth_user"

#     cursor.execute(sql2)

#     row = cursor.fetchall()

#     req = request.get_json()
#     u_id = req['userRequest']['user']['id']
#     print(u_id)

#     block_id = req['userRequest']['block']['id']

#     f1_add = req["action"]["detailParams"]["sys_text"]["value"]

#     query = "insert into form1(u_id,f1_address,date) values(%s,%s,NOW())"

#     cursor.execute(query, (u_id, f1_add))

#     global fid
#     fid = cursor.lastrowid

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 다음 질문으로 이동하시겠습니까?",
#                            "buttons": [{
#                                "action": "block",
#                                "label": "다음질문으로",
#                                "blockId": "5d92fd2292690d0001a423ee"
#                            }, FIRST_BTN
#                            ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f1_2', methods=['POST'])
# def f1_2():

#     req = request.get_json()
#     print(req, file=sys.stderr)
#     print((u_id))
#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f1_det = req["action"]["detailParams"]["sys_text"]["value"]

#     query = """update form1 set f1_det = %s where fid = %s"""

#     val = (f1_det, fid)

#     cursor.execute(query, val)

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 다음 질문으로 이동하시겠습니까?",
#                            "buttons": [{
#                                "action": "block",
#                                "label": "다음질문으로",
#                                "blockId": "5d9322c6b617ea00012ae213"
#                            }, FIRST_BTN
#                            ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f1_3', methods=['POST'])
# def f1_3():
#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f1_budget = req["action"]["detailParams"]["sys_text"]["value"]

#     query = """update form1 set f1_budget = %s where fid = %s"""

#     val = (f1_budget, fid)

#     cursor.execute(query, val)

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 다음 질문으로 이동하시겠습니까?",
#                            "buttons": [{
#                                "action": "block",
#                                "label": "다음질문으로",
#                                "blockId": "5d9429a98192ac000115340d"
#                            }, FIRST_BTN
#                            ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f1_4', methods=['POST'])
# def f1_4():
#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f1_concept = req["action"]["detailParams"]["sys_text"]["value"]

#     query = """update form1 set f1_concept = %s where fid = %s"""

#     val = (f1_concept, fid)

#     cursor.execute(query, val)

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 다음 질문으로 이동하시겠습니까?",
#                            "buttons": [{
#                                "action": "block",
#                                "label": "다음질문으로",
#                                "blockId": "5d942a1a92690d0001a42a21"
#                            }, FIRST_BTN
#                            ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f1_5', methods=['POST'])
# def f1_5():
#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f1_date = req["action"]["detailParams"]["sys_text"]["origin"]

#     query = """update form1 set f1_date = %s where fid = %s"""

#     val = (f1_date, fid)

#     cursor.execute(query, val)

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 추가 희망사항이 있으신가요? 없으면 홈으로 이동해주세요",
#                            "buttons": [{
#                                "action": "block",
#                                "label": "다음질문으로",
#                                "blockId": "5d942b528192ac0001153481"
#                            }, FIRST_BTN
#                            ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f1_6', methods=['POST'])
# def f1_6():
#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f1_extra = req["action"]["detailParams"]["sys_text"]["value"]

#     query = """update form1 set f1_extra = %s where fid = %s"""

#     val = (f1_extra, fid)

#     cursor.execute(query, val)

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 곧 답변 드리겠습니다.",
#                            "buttons": [FIRST_BTN
#                                        ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f2_1', methods=['POST'])
# def f2_1():
#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f2_date = req["action"]["detailParams"]["sys_text"]["value"]

#     query = "insert into form2(u_id,f2_date,date) values(%s,%s,NOW())"

#     cursor.execute(query, (u_id, f2_date))

#     global fid
#     fid = cursor.lastrowid

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 다음 질문으로 이동하시겠습니까?",
#                            "buttons": [{
#                                "action": "block",
#                                "label": "다음질문으로",
#                                "blockId": "5d94436f8192ac0001153603"
#                            }, FIRST_BTN
#                            ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f2_2', methods=['POST'])
# def f2_2():

#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f2_money = req["action"]["detailParams"]["sys_text"]["value"]

#     query = """update form2 set f2_money = %s where fid = %s"""

#     val = (f2_money, fid)

#     cursor.execute(query, val)

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 다음 질문으로 이동하시겠습니까?",
#                            "buttons": [{
#                                "action": "block",
#                                "label": "다음질문으로",
#                                "blockId": "5d9443968192ac0001153607"
#                            }, FIRST_BTN
#                            ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f2_3', methods=['POST'])
# def f2_3():
#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f2_type = req["action"]["detailParams"]["sys_text"]["value"]

#     query = """update form2 set f2_type = %s where fid = %s"""

#     val = (f2_type, fid)

#     cursor.execute(query, val)

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 추가 희망사항이 있으신가요? 없으면 홈으로 이동해주세요",
#                            "buttons": [{
#                                "action": "block",
#                                "label": "다음질문으로",
#                                "blockId": "5d9443c68192ac000115360d"
#                            }, FIRST_BTN
#                            ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f2_4', methods=['POST'])
# def f2_4():
#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f2_extra = req["action"]["detailParams"]["sys_text"]["value"]

#     query = """update form2 set f2_extra = %s where fid = %s"""

#     val = (f2_extra, fid)

#     cursor.execute(query, val)

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 곧 답변 드리겠습니다.",
#                            "buttons": [FIRST_BTN
#                                        ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f3_1', methods=['POST'])
# def f3_1():
#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f3_concept = req["action"]["detailParams"]["sys_text"]["value"]

#     query = "insert into form3(u_id,f3_concept,date) values(%s,%s,date())"

#     cursor.execute(query, (u_id, f3_concept))

#     global fid
#     fid = cursor.lastrowid

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 추가 희망사항이 있으신가요? 없으면 홈으로 이동해주세요",
#                            "buttons": [{
#                                "action": "block",
#                                "label": "다음질문으로",
#                                "blockId": "5d944881ffa7480001da9fdf"
#                            }, FIRST_BTN
#                            ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f3_2', methods=['POST'])
# def f3_2():
#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f3_extra = req["action"]["detailParams"]["sys_text"]["value"]

#     query = """update form3 set f3_extra = %s where fid = %s"""

#     val = (f3_extra, fid)

#     cursor.execute(query, val)

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 곧 답변 드리겠습니다.",
#                            "buttons": [FIRST_BTN
#                                        ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f4', methods=['POST'])
# def f4():
#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f4_money = req["action"]["detailParams"]["sys_text"]["value"]

#     query = "insert into form4(u_id,f4_money,date) values(%s,%s,NOW())"

#     cursor.execute(query, (u_id, f4_money))

#     global fid
#     fid = cursor.lastrowid

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 다음 질문으로 이동하시겠습니까?",
#                            "buttons": [{
#                                "action": "block",
#                                "label": "다음질문으로",
#                                "blockId": "5d94489dffa7480001da9fe4"
#                            }, FIRST_BTN
#                            ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f4_1', methods=['POST'])
# def f4_1():

#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f4_type = req["action"]["detailParams"]["sys_text"]["value"]

#     query = """update form4 set f4_type = %s where fid = %s"""

#     val = (f4_type, fid)

#     cursor.execute(query, val)

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 다음 질문으로 이동하시겠습니까?",
#                            "buttons": [{
#                                "action": "block",
#                                "label": "다음질문으로",
#                                "blockId": "5d9448d58192ac000115364e"
#                            }, FIRST_BTN
#                            ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f4_2', methods=['POST'])
# def f4_2():

#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f4_year = req["action"]["detailParams"]["sys_text"]["value"]

#     query = """update form4 set f4_year = %s where fid = %s"""

#     val = (f4_year, fid)

#     cursor.execute(query, val)

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 다음 질문으로 이동하시겠습니까?",
#                            "buttons": [{
#                                "action": "block",
#                                "label": "다음질문으로",
#                                "blockId": "5d944902ffa7480001da9fe8"
#                            }, FIRST_BTN
#                            ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f4_3', methods=['POST'])
# def f4_3():
#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f4_date = req["action"]["detailParams"]["sys_text"]["value"]

#     query = """update form4 set f4_date = %s where fid = %s"""

#     val = (f4_date, fid)

#     cursor.execute(query, val)

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 추가 희망사항이 있으신가요? 없으면 홈으로 이동해주세요",
#                            "buttons": [{
#                                "action": "block",
#                                "label": "다음질문으로",
#                                "blockId": "5d9449388192ac0001153655"
#                            }, FIRST_BTN
#                            ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f4_4', methods=['POST'])
# def f4_4():
#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f4_extra = req["action"]["detailParams"]["sys_text"]["value"]

#     query = """update form4 set f4_extra = %s where fid = %s"""

#     val = (f4_extra, fid)

#     cursor.execute(query, val)

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 곧 답변 드리겠습니다.",
#                            "buttons": [FIRST_BTN
#                                        ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f5_1', methods=['POST'])
# def f5_1():
#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f5_all = req["action"]["detailParams"]["sys_text"]["value"]

#     query = "insert into form5(u_id,f5_all,date) values(%s,%s,NOW())"

#     cursor.execute(query, (u_id, f5_all))

#     global fid
#     fid = cursor.lastrowid

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 추가 희망사항이 있으신가요? 없으면 홈으로 이동해주세요",
#                            "buttons": [{
#                                "action": "block",
#                                "label": "다음질문으로",
#                                "blockId": "5d9449888192ac000115365c"
#                            }, FIRST_BTN
#                            ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f5_2', methods=['POST'])
# def f5_2():
#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f5_extra = req["action"]["detailParams"]["sys_text"]["value"]

#     query = """update form5 set f5_extra = %s where fid = %s"""

#     val = (f5_extra, fid)

#     cursor.execute(query, val)

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 곧 답변 드리겠습니다.",
#                            "buttons": [FIRST_BTN
#                                        ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f6_1', methods=['POST'])
# def f6_1():

#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f6_type = req["action"]["detailParams"]["sys_text"]["value"]
#     query = "insert into form6(u_id,f6_type,date) values(%s,%s,NOW())"

#     cursor.execute(query, (u_id, f6_type))

#     global fid
#     fid = cursor.lastrowid

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 다음 질문으로 이동하시겠습니까?",
#                            "buttons": [{
#                                "action": "block",
#                                "label": "다음질문으로",
#                                "blockId": "5d944a0192690d0001a42cbe"
#                            }, FIRST_BTN
#                            ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f6_2', methods=['POST'])
# def f6_2():

#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f6_detail = req["action"]["detailParams"]["sys_text"]["value"]

#     query = """update form6 set f6_detail = %s where fid = %s"""

#     val = (f6_detail, fid)

#     cursor.execute(query, val)

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 추가 희망사항이 있으신가요? 없으면 홈으로 이동해주세요",
#                            "buttons": [{
#                                "action": "block",
#                                "label": "다음질문으로",
#                                "blockId": "5d944a2a92690d0001a42cc1"
#                            }, FIRST_BTN
#                            ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


# @app.route('/f6_3', methods=['POST'])
# def f6_3():
#     req = request.get_json()
#     print(req, file=sys.stderr)

#     if u_id == 0:
#         res = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "basicCard": {
#                             "title": "로그인 세션이 만료되었습니다. 홈으로 이동해서 다시 로그인해주세요",
#                             "buttons": [GO_FIRST_BTN]
#                         }
#                     }
#                 ]
#             }
#         }

#         return res

#     block_id = req['userRequest']['block']['id']

#     f6_extra = req["action"]["detailParams"]["sys_text"]["value"]

#     query = """update form6 set f6_extra = %s where fid = %s"""

#     val = (f6_extra, fid)

#     cursor.execute(query, val)

#     res = {"version": "2.0",
#            "template": {
#                "outputs": [
#                    {
#                        "basicCard": {
#                            "title": "입력이 완료 되었습니다. 곧 답변 드리겠습니다.",
#                            "buttons": [FIRST_BTN
#                                        ]
#                        }
#                    }
#                ]
#            }
#            }

#     return jsonify(res)


@app.route('/question', methods=['POST'])
def question():

    req = request.get_json()
    print(req, file=sys.stderr)

    block_id = req['userRequest']['block']['id']

    q_content = req["action"]["detailParams"]["sys_text"]["value"]
    query = "insert into question(q_content) values(%s)"

    cursor.execute(query, (q_content))

    res = {"version": "2.0",
           "template": {
               "outputs": [
                   {
                       "basicCard": {
                           "title": "입력이 완료 되었습니다.  ",

                       }
                   }
               ]
           }
           }

    return jsonify(res)


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True, debug='on', port=8000)
