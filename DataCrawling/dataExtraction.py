import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from collections import Counter

#bs4를 사용하여 가장 최근 로또 회차를 불러온다
r = requests.get('https://dhlottery.co.kr/gameResult.do?method=byWin') #동행복권 사이트에 접속한다
html = r.text
jsonload = ""
soup = BeautifulSoup(html, 'html.parser')
recent_lotto_number=soup.select('div > .win_result > h4 > strong') #가장 최근의 로또 결과를 출력하는 html tag을 찾는다
recent_lotto_number = recent_lotto_number[0].text.replace("회", "")

#모든 로또 정보를 API를 통해서 받아온다 그리고 pandas를 통해 원하는 형태의 csv로 가공한다
No1 = []
No2 = []
No3 = []
No4 = []
No5 = []
No6 = []
bonusNo = []

for i in range(1, int(recent_lotto_number)+1):
    #API를 통해 역대 로또 회차별 번호 결과를 가지고 온다
    response = requests.get("https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="+str(i)).json()
    No1.append(response['drwtNo1'])
    No2.append(response['drwtNo2'])
    No3.append(response['drwtNo3'])
    No4.append(response['drwtNo4'])
    No5.append(response['drwtNo5'])
    No6.append(response['drwtNo6'])
    bonusNo.append(response['bnusNo'])

    print(i, response['drwtNo1'])

lotto_result = {"Num1":No1, "Num2":No2, "Num3":No3, "Num4":No4, "Num5":No5, "Num6":No6, "bnsNum":bonusNo} #딕션너리 형태로 결과를 저장한다

lotto_data = pd.DataFrame(lotto_result) #결과를 데이터프레임 형태로 바꾼다
lotto_data.index = np.arange(1, len(lotto_data) + 1) #인덱스를 0->1 시작으로 바꾼다 (회차와 일치하게)
lotto_data.to_csv("./DataCollection/lottoResultAllTime.csv")