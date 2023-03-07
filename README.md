# Crawling_Telegram (Base_Version)
- Ubuntu 20.04 LTS
- Python 3.8.10
- PostgreSQL
#
- Directory
```bash
├──etc
│   ├──test_table.txt
│   ├──test.csv
├──lib
│   ├──crawling.py
│   ├──database.py
│   ├──make_data.py
│   ├──settings.py
│   ├──telegram.py
├──tmp_json
│   ├──test1.json
│   ├──test2.json
├──requirements.txt
├──run.py
```
# 
   - 수출입 데이터 그래프 텔레그램 전송 자동화 스크립트
   - 제작기간
      - 약 2주 소요
   - 서버 구축, DB, 스크립트 개발
      - 다른 업종의 직무와 협업
   - 이후 버전은 협업자의 아이디어가 추가 (Doing)
- URL : https://www.bandtrass.or.kr/customs/total.do?command=CUS001View&viewCode=CUS00401
#
1. lib/settings에 기본 설정
   - DB_INFO
      - ip,port 등 기본 정보 등재
   - TELEGRAM_BOT_ID & TELEGRAM_CHAT_ID
      - 텔레그램에서 봇 생성 후 bot_id를 획득
      - 원하는 채팅방에 bot을 입장
      - https://api.telegram.org/bot<XXX:YYYY>/getUpdates 를 주소창에 입력
      - api를 통해 chat_id 확인
   - 적절하게 path 수정

2. 그래프는 작년치 데이터랑 비교 하기때문에 미리 DB 적재 해야됨
   - etc/test_table.txt
      - 예제에 사용되는 table 정보
   - etc/test.csv
      - 데이터 예시

3. URL에서 확인하고 싶은 hscode를 json 형식으로 만든뒤 tmp_json 폴더에 넣는다
   - tmp_json/test1.json
      - json 예시
   - settings에 json을 수집할 수있는 기본 폴더가 설정 되어있다.
   - 기본 폴더 or 특정 폴더에 json만 있다면 나눠서 수집이 가능하다

4. 실행
   - python3 run.py
      - 기본 설정된 json 폴더가 아닌 원하는 폴더의 절대 경로를 입력하면 그 폴더의 json이 수집된다
      - python3 run.py /tmp/json_tmp

# 특이사항
   - 매달 1, 11, 21일 1130에 crontab으로 실행되는 형식으로 제작
      - 날짜별로 DB에 적재되는 방식이 다름
          - 1일 - Update
          - 11일 - Insert
          - 21일 - Update
   - 사진을 저장후 보내는 형식이라 저장소 따로 구분
      - 스크립트 실행 시 자동 생성
   - 그래프 생성시 한글깨짐 방지 font는 os마다 상이함
      - lib/make_data.py > 64번째줄 
