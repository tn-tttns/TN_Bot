import requests, os, csv, time, traceback, datetime, random
import graphql, utills
from keep_alive import keep_alive

pre_id = 0
active = True

with requests.Session() as s:
  bot = utills.Bot(s)

  def createComment(text, image=None):
    global pre_id
    if active == True:
      if image == None:
        s.post('https://playentry.org/graphql', headers=bot.headers, json={'query': graphql.createComment, "variables": {"content": text, "target": bot.id, "targetSubject": "discuss", "targetType": "individual"}})
      else:
        s.post('https://playentry.org/graphql', headers=bot.headers,
               json={
                 'query': graphql.createComment,
                 "variables": {
                   "content": text,
                   "image": image,
                   "target": bot.id,
                   "targetSubject": "discuss",
                   "targetType": "individual"
                 }
               })
      pre_id = bot.id

  def createStory(text):
    s.post('https://playentry.org/graphql', headers=bot.headers,
            json={
              'query': graphql.createStory,
              "variables": {
                "content": text
              }
            })

  def openAdmin():
    f = open('gitignore/admin.csv', 'r')
    reader = csv.reader(f)
    output = []
    for i in reader:
      output.append(i)
    f.close()
    return output[0]

  def plusAdmin():
    f = open('gitignore/admin.csv', 'w')
    a = csv.writer(f, delimiter=',')
    a.writerows([adminList])
    f.close()

  keep_alive()
  print('티엔봇 작동 시작')

  while True:
    try:
      time.sleep(0.1)
      bot.setting()
      if pre_id != bot.id and len(bot.text)!=0:
        if bot.text[:2] in ['ㅌ ', 't ', 'T '] or bot.text[:4] in ['ㅌㅇㅂ ', '티엔봇 ', 'tnb ', 'TNB ', 'TNb ']:
          commend = bot.text[bot.text.index(' ')+1:]
          # 일반 명령어
          try:
            createComment(utills.commendList[commend])

          except:
            # 혼동되는 명령어 안내
            if commend[:5] == '세부정보 ':
              createComment("이전의 'ㅌ 세부정보' 기능은 'ㅌ 정보' 명령어로 통합되었어요!")
            if commend[:7] == '닉네임 정보 ':
              createComment("특정 유저의 정보를 알고 싶나요? 'ㅌ 정보 {닉네임}' 명령어를 사용해보세요!")
            if commend[:10] == '닉네임으로 글찾기 ':
              createComment("특정 유저의 글을 찾고 싶나요? 'ㅌ 글찾기 {닉네임}' 명령어를 사용해보세요!")
            if commend[:11] == '닉네임으로 노팁찾기 ':
              createComment("특정 유저의 노팁을 찾고 싶나요? 'ㅌ 노팁찾기 {닉네임}' 명령어를 사용해보세요!")

            # 추가 동작이 필요한 명령어
            elif commend == '팀백업 한마디':
              createComment(
                random.choice([
                  '"지나간 과거를 보며 뒤돌기보다는 미래를 위해 앞으로 향하자" - Team FrontUP',
                  '"모두가 올라갈 방법을 찾을 때 아래쪽을 돌아보자" - Team BackDOWN',
                  '"모두가 백업을 생각할때, 프론트다운을 떠올려라" - Team FrontDOWN'
                ]))
            elif commend in ['폭발', '폭8', '자폭']:
              createComment('폭8!!!!! 퍼퍼퍼버어어버ㅓㅍ어ㅓ어', '61de946f1e65f8fcf9015350')
            elif commend in ['안녕', '안녕!', '안녕?', '반가워']:
              createComment('안녕하세요!', '63e1eea87b794ac993acd114')

            elif commend[:3] == '유찾 ':
              rpl = ''
              myPage = bot.userSearchNick(commend[3:])
              if myPage != None:
                rpl = f'playentry.org/profile/{myPage} (닉네임)'
              myPage = bot.userSearchId(commend[3:])
              if rpl != '' and myPage != None:
                if rpl[22:46] == myPage:
                  rpl = f'playentry.org/profile/{myPage} (닉네임, 아이디)'
                else:
                  rpl = f'{rpl}, playentry.org/profile/{myPage} (아이디)'
              elif myPage != None:
                rpl = f'playentry.org/profile/{myPage} (아이디)'
              if rpl == '':
                rpl = f'{commend[3:]} 닉네임/아이디를 가진 유저를 찾을 수 없어요.'
              else:
                rpl = f'{commend[3:]}님의 마이페이지 주소는 {rpl} 이에요!'
              rplPlus = ''
              myPage = bot.userSearchNick(commend[3:] + '_')
              if myPage != None:
                rplPlus = f'playentry.org/profile/{myPage} ({commend[3:]}_)'
              myPage = bot.userSearchNick(commend[3:] + 'ㅤ')
              if myPage != None:
                if rplPlus == '':
                  rplPlus = f'playentry.org/profile/{myPage} ({commend[3:]}ㅤ)'
                else:
                  rplPlus = f'{rplPlus}, playentry.org/profile/{myPage} ({commend[3:]}ㅤ)'
              myPage = bot.userSearchNick(commend[3:] + '_ㅤ')
              if myPage != None:
                if rplPlus == '':
                  rplPlus = f'playentry.org/profile/{myPage} ({commend[3:]}_ㅤ)'
                else:
                  rplPlus = f'{rplPlus}, playentry.org/profile/{myPage} ({commend[3:]}_ㅤ)'
              myPage = bot.userSearchNick(commend[3:] + 'ㅤㅤ')
              if myPage != None:
                if rplPlus == '':
                  rplPlus = f'playentry.org/profile/{myPage} ({commend[3:]}ㅤㅤ)'
                else:
                  rplPlus = f'{rplPlus}, playentry.org/profile/{myPage} ({commend[3:]}ㅤㅤ)'
              try:
                myPage = bot.userSearchId(utills.user[commend[3:]])
                if myPage != None:
                  if rplPlus == '':
                    rplPlus = f'playentry.org/profile/{myPage} ({utills.user[commend[3:]]})'
                  else:
                    rplPlus = f'{rplPlus}, playentry.org/profile/{myPage} ({utills.user[commend[3:]]})'
              except:
                pass
              if rplPlus != '':
                rpl = f'{rpl} 혹시 이 유저를 찾으시려던 건가요? {rplPlus}'
              if commend[3:] in ['레몬봇', 'lemonbpt', 'Lemon봇', 'lemonbot']:
                rpl = f'{rpl} .....그런데 레몬봇을 왜 찾으시나요? 여기 티엔봇이 있답니다!'
              createComment(rpl)

            elif commend == '프사':
              profileImage = bot.profileImage(bot.authorId)
              createComment(f'{bot.authorNick}님의 프로필 사진이에요!', profileImage)

            elif commend[:3] == '프사 ':
              myPage = bot.userSearchNick(commend[3:])
              if myPage == None:
                createComment(f'{commend[3:]} 닉네임을 가진 유저를 찾을 수 없어요.')
              else:
                profileImage = bot.profImgNick(myPage)
                createComment(f'{commend[3:]}님의 프로필 사진이에요!', profileImage)

            elif commend == '배사':
              bgImage = bot.bgImage(bot.authorId)
              createComment(f'{bot.authorNick}님의 배경 사진이에요!', bgImage)

            elif commend[:3] == '배사 ':
              myPage = bot.userSearchNick(commend[3:])
              if myPage == None:
                createComment(f'{commend[3:]} 닉네임을 가진 유저를 찾을 수 없어요.')
              else:
                bgImage = bot.bgImage(myPage)
                createComment(f'{commend[3:]}님의 배경 사진이에요!', bgImage)

            elif commend == '정보':
              projectCnt, like, comment, view, status, qna, tip, free, popular, staff, mostLike, mostComment, mostView = bot.info(bot.authorId)
              if projectCnt == 0:
                createComment(f'{bot.authorNick}님의 작품이 없어요. playentry.org/ws/new 에서 새 작품을 만들어 보세요! 커뮤니티 글 {qna+tip+free}개 중 묻고 답하기 {qna}개, 노하우&팁 {tip}개, 엔트리 이야기 {free}개입니다.')
              else:
                createComment(f'{bot.authorNick}님의 작품 {projectCnt}개의 총 좋아요 수는 {like}개, 댓글 수는 {comment}개, 조회수는 {view}회 입니다. 좋아요 가장 많은 작품 playentry.org/project/{mostLike}, 댓글 가장 많은 작품 playentry.org/project/{mostComment}, 조회수 가장 많은 작품 playentry.org/project/{mostView}. 인작 {popular}개, 스선 {staff}개. 커뮤니티 글 {qna+tip+free}개 중 묻고 답하기 {qna}개, 노하우&팁 {tip}개, 엔트리 이야기 {free}개입니다.')

            elif commend == '좋아요수':
              projectCnt, like, comment, view, status, qna, tip, free, popular, staff, mostLike, mostComment, mostView = bot.info(bot.authorId)
              if projectCnt == 0:
                createComment(f'{bot.authorNick}님의 작품이 없어요. playentry.org/ws/new 에서 새 작품을 만들어 보세요!')
              else:
                createComment(f'{bot.authorNick}님의 작품 {projectCnt}개의 총 좋아요 수는 {like}개에요!')

            elif commend == '조회수':
              projectCnt, like, comment, view, status, qna, tip, free, popular, staff, mostLike, mostComment, mostView = bot.info(bot.authorId)
              if projectCnt == 0:
                createComment(f'{bot.authorNick}님의 작품이 없어요. playentry.org/ws/new 에서 새 작품을 만들어 보세요!')
              else:
                createComment(f'{bot.authorNick}님의 작품 {projectCnt}개의 총 조회수는 {view}회에요!')

            elif commend == '댓글수':
              projectCnt, like, comment, view, status, qna, tip, free, popular, staff, mostLike, mostComment, mostView = bot.info(bot.authorId)
              if projectCnt == 0:
                createComment(f'{bot.authorNick}님의 작품이 없어요. playentry.org/ws/new 에서 새 작품을 만들어 보세요!')
              else:
                createComment(f'{bot.authorNick}님의 작품 {projectCnt}개의 총 댓글 수는 {comment}개에요!')

            elif commend[:3] == '정보 ':
              if commend[3:]=='TN_Bot':
                createComment('저 자신의 정보는 아직 조회할 수 없어요. 조금만 기다려주시면 곧 개선할게요!')
              else:
                myPage = bot.userSearchNick(commend[3:])
                if myPage==None:
                  createComment(f'{commend[3:]} 닉네임을 가진 유저를 찾을 수 없어요.')
                else:
                  projectCnt, like, comment, view, status, qna, tip, free, popular, staff, mostLike, mostComment, mostView = bot.info(myPage)
                  if status == "USE": status = ''
                  elif status == "WARN": status = '현재 1차 또는 2차정지 상태입니다.'
                  else: status = '영구정지 상태입니다.'
                  if projectCnt == 0:
                    createComment(f'{commend[3:]}님의 작품이 없어요. playentry.org/ws/new 에서 새 작품을 만들어 보세요! 커뮤니티 글 {qna+tip+free}개 중 묻고 답하기 {qna}개, 노하우&팁 {tip}개, 엔트리 이야기 {free}개입니다. {status}')
                  else:
                    createComment(f'{commend[3:]}님의 작품 {projectCnt}개의 총 좋아요 수는 {like}개, 댓글 수는 {comment}개, 조회수는 {view}회 입니다. 좋아요 가장 많은 작품 playentry.org/project/{mostLike}, 댓글 가장 많은 작품 playentry.org/project/{mostComment}, 조회수 가장 많은 작품 playentry.org/project/{mostView}. 인작 {popular}개, 스선 {staff}개. 커뮤니티 글 {qna+tip+free}개 중 묻고 답하기 {qna}개, 노하우&팁 {tip}개, 엔트리 이야기 {free}개입니다. {status}')

            elif commend[:5] == '좋아요수 ':
              myPage = bot.userSearchNick(commend[5:])
              if myPage==None:
                createComment(f'{commend[5:]} 닉네임을 가진 유저를 찾을 수 없어요.')
              else:
                projectCnt, like, comment, view, status, qna, tip, free, popular, staff, mostLike, mostComment, mostView = bot.info(myPage)
                if projectCnt == 0:
                  createComment(f'{commend[5:]}님의 작품이 없어요.')
                else:
                  createComment(f'{commend[5:]}님의 작품 {projectCnt}개의 총 좋아요 수는 {like}개에요!')

            elif commend[:4] == '조회수 ':
              myPage = bot.userSearchNick(commend[4:])
              if myPage==None:
                createComment(f'{commend[4:]} 닉네임을 가진 유저를 찾을 수 없어요.')
              else:
                projectCnt, like, comment, view, status, qna, tip, free, popular, staff, mostLike, mostComment, mostView = bot.info(myPage)
                if projectCnt == 0:
                  createComment(f'{commend[4:]}님의 작품이 없어요.')
                else:
                  createComment(f'{commend[4:]}님의 작품 {projectCnt}개의 총 조회수는 {view}회에요!')

            elif commend[:4] == '댓글수 ':
              myPage = bot.userSearchNick(commend[4:])
              if myPage==None:
                createComment(f'{commend[4:]} 닉네임을 가진 유저를 찾을 수 없어요.')
              else:
                projectCnt, like, comment, view, status, qna, tip, free, popular, staff, mostLike, mostComment, mostView = bot.info(myPage)
                if projectCnt == 0:
                  createComment(f'{commend[4:]}님의 작품이 없어요.')
                else:
                  createComment(f'{commend[4:]}님의 작품 {projectCnt}개의 총 댓글 수는 {comment}개에요!')

            elif commend[:5] == '정지여부 ':
              myPage = bot.userSearchNick(commend[5:])
              if myPage==None:
                createComment(f'{commend[5:]} 닉네임을 가진 유저를 찾을 수 없어요.')
              else:
                projectCnt, like, comment, view, status, qna, tip, free, popular, staff, mostLike, mostComment, mostView = bot.info(myPage)
                if status == "USE": status = '정지 상태가 아닙니다.'
                elif status == "WARN": status = '현재 1차 또는 2차정지 상태입니다.'
                else: status = '영구정지 상태입니다.'
                createComment(f'{commend[5:]}님은 {status}')

            elif commend[:6] == '커뮤니티수 ':
              myPage = bot.userSearchNick(commend[6:])
              if myPage==None:
                createComment(f'{commend[6:]} 닉네임을 가진 유저를 찾을 수 없어요.')
              else:
                projectCnt, like, comment, view, status, qna, tip, free, popular, staff, mostLike, mostComment, mostView = bot.info(myPage)
                createComment(f'{commend[6:]}님의 커뮤니티 글 {qna+tip+free}개 중 묻고 답하기 {qna}개, 노하우&팁 {tip}개, 엔트리 이야기 {free}개입니다.')

            elif commend == '랜덤작':
              project, name, nick, des = bot.ranProject()
              createComment(f'{nick}님의 {name} 작품은 어때요? playentry.org/project/{project} {des}')

            elif commend[:4] == '랜덤작 ':
              if commend[4:] in ['게임', '생활과 도구', '스토리텔링', '예술', '지식 공유', '기타']:
                project, name, nick, des = bot.ranProject(commend[4:])
                createComment(f'{nick}님의 {name} 작품은 어때요? playentry.org/project/{project} {des}')
              else:
                createComment('게임, 생활과 도구, 스토리텔링, 예술, 지식 공유, 기타 중 하나의 카테고리를 선택해주세요!')

            # 관리 명령어
            elif commend=='나 사랑해?':
              adminList=openAdmin()
              if bot.authorId in adminList:
                createComment('저는 당연히 티엔님을 사랑해요!')
              else:
                love=['한지민을', '또이를', '티엔님을', '개발자님을', '영자님을', '운영자님을', '엔프님을', '엔트리를', '엔트리봇을', 'hjm13_을', '히짐을', 'ddoeey123을', 'ZerO를', 'entryfriends님을']
                createComment(f'아뇨, 전 {random.choice(love)} 사랑해요^^')

            elif commend[:7] == '관리자 추가 ':
              adminList = openAdmin()
              if bot.authorId in adminList:
                if commend[7:] in adminList:
                  createComment('이미 관리자 목록에 추가되어 있어요.')
                else:
                  adminList.append(commend[7:])
                  plusAdmin()
                  createComment('관리자 추가가 완료되었습니다.')
              else:
                createComment('관리자만 사용할 수 있는 명령어입니다.')

            elif commend == '시작':
              adminList = openAdmin()
              if bot.authorId in adminList:
                if active == True:
                  createComment('이미 작동하고 있습니다.')
                else:
                  active = True
                  createComment('티엔봇 작동을 시작합니다.')
                  createStory('티엔봇 작동을 시작합니다.')
              else:
                createComment('관리자만 사용할 수 있는 명령어입니다.')

            elif commend == '중지':
              adminList = openAdmin()
              if bot.authorId in adminList:
                if active == True:
                  createComment('티엔봇 작동을 중지합니다.')
                  active = False
                  createStory('티엔봇 작동을 중지합니다.')
              else:
                createComment('관리자만 사용할 수 있는 명령어입니다.')

            # 명령어 끝
            else:
              createComment('아직 지원하지 않는 명령어에요. 명령어 관련 제안이 있다면 이 작품에 알려주세요! naver.me/5UGa0Vxs')
        elif bot.text == 'ㅌ':
          createComment('부르셨나요?', '63e1eea87b794ac993acd114')
        elif bot.text[0] == 'ㅌ' and bot.text[:4]!='ㅌㅈㅅㄱ' and bot.text[:3]!='ㅌㅣ프':
          createComment("절 부르려고 하셨나요? 'ㅌ' 뒤에 띄어쓰기를 해주세요!", '63e1eea87b794ac993acd114')

    # 에러 출력
    except:
      print('\n========== ERROR ==========')
      print(f'\nTime: {datetime.datetime.now()}')
      print(f'Text URL: playentry.org/community/entrystory/{bot.id}')
      print(f'Text: {bot.text}\n')
      print(traceback.format_exc())
      print('===========================')
