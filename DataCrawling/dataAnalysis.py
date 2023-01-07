import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from collections import Counter
import os, json, sys, random, ast


No1 = [] 
No2 = []
No3 = []
No4 = []
No5 = []
No6 = []
bonusNo = []
count = 0

def createLottoResultAllTime():
    resultCSV = pd.read_csv("./DataCollection/lottoResultAllTime.csv")

    No1 = Counter(resultCSV["Num1"])
    No2 = Counter(resultCSV["Num2"])
    No3 = Counter(resultCSV["Num3"])
    No4 = Counter(resultCSV["Num4"])
    No5 = Counter(resultCSV["Num5"])
    No6 = Counter(resultCSV["Num6"])
    bonusNo = Counter(resultCSV["bnsNum"])
    #print(No1, "\n", dict(No1))
    frequencyData = {
        "freqeuncy" : {
            "Num1": No1.most_common(), 
            "Num2": No2.most_common(), 
            "Num3": No3.most_common(), 
            "Num4": No4.most_common(), 
            "Num5": No5.most_common(), 
            "Num6": No6.most_common(), 
            "bnsNum": bonusNo.most_common()}, 
        "datasetNum" : len(resultCSV)
        }

    script_dir = os.path.dirname(__file__)
    #print(frequencyData, script_dir)
    file_path = os.path.join(script_dir, "../DataCollection/frequencyData.json")
    with open(file_path, 'w') as json_file:
            json.dump(frequencyData, json_file, sort_keys=True, indent=4)

def LottoResultAllTimeDownload():
    resultCSV = pd.read_csv("./DataCollection/lottoResultAllTime.csv")

    No1 = resultCSV["Num1"]
    No2 = resultCSV["Num2"]
    No3 = resultCSV["Num3"]
    No4 = resultCSV["Num4"]
    No5 = resultCSV["Num5"]
    No6 = resultCSV["Num6"]
    bonusNo = resultCSV["bnsNum"]
    #print(No1, "\n", dict(No1))
    frequencyData = {
        "freqeuncy" : {
            "Num1": No1, 
            "Num2": No2, 
            "Num3": No3, 
            "Num4": No4, 
            "Num5": No5, 
            "Num6": No6, 
            "bnsNum": bonusNo}, 
        "datasetNum" : len(resultCSV)
    }

    script_dir = os.path.dirname(__file__)
    #print(frequencyData, script_dir)
    file_path = os.path.join(script_dir, "../DataCollection/frequencyDataDownload.json")
    with open(file_path, 'w') as json_file:
            json.dump(frequencyData, json_file, sort_keys=True, indent=4)

    print("done")

def loadLottoResultAllTime():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "../DataCollection/frequencyData.json")
    jsonfile = open(file_path, 'r')
    data = json.load(jsonfile)
    print(json.dumps(data))

def createPieChart(input):
    resultCSV = pd.read_csv("./DataCollection/lottoResultAllTime.csv")
    resultCSV = pd.DataFrame(resultCSV)

    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "../DataCollection/frequencyData.json")
    jsonfile = open(file_path, 'r')
    data = json.load(jsonfile)
    
    pieCharNo = eval(input).most_common()

    numValue = []
    sizes = []
    rest = 0
    for i in range(10):
        numValue.append(str(pieCharNo[i][0]))
        percentage = round(100 * pieCharNo[i][1] / data["datasetNum"], 2)
        rest += percentage
        sizes.append(percentage)
    rest = 100 - rest
    numValue.append("Other")
    #print(rest)
    sizes.append(round(rest, 2))

    wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}
    plt.pie(sizes, labels=numValue, autopct='%1.1f%%', wedgeprops=wedgeprops) #파이차트 이미지 중간 비우기
    #이미지 사이즈 조절
    figure = plt.gcf() 
    figure.set_size_inches(8, 8)
    #이미지 저장
    plt.savefig('./DataCollection/{input}.png'.format(input = input), dpi=200, transparent=True)
    plt.close()

#반복된 정보 알아내기, 예를 들어서 하나의 로또에 같은 숫자가 2번 있는지, 같은 로또 번호가 당첨된적 있는지
def checkifrepeated():
    resultCSV = pd.read_csv("./DataCollection/lottoResultAllTime.csv")

    u, c = np.unique(resultCSV, axis=0, return_counts=True)
    print((c>1).any())

# 데이터 추출 필요 정보 기능들
# 랜덤 추천 로또 번호 생성 (최대 5개) 그리고 최근 100개랑 비교해서 적중률 테스트
# 데이터 범위 설정 기능
# 숫자별 가장 빈도 높은 로또들 번호들 사이에서 뽑기 (n개 사용자 지정, 비율 조정/x)
# 숫자별 가장 빈도 낮은 로또들 번호들 사이에서 뽑기 (n개 사용자 지정, 비율 조정/x)
# 최근 데이터 n개 기준
# 내가 원하는 숫자 입력하고 비교


#https://www.machinelearningplus.com/pandas/pandas-duplicated/
#https://stackoverflow.com/questions/70506590/i-want-to-check-if-there-are-any-identical-rows-in-a-matrix
#https://www.google.com/search?q=pandas+numpy+check+if+there+is+repeated+row+and+return+value&newwindow=1&sxsrf=ALiCzsaS-gqhtNmV2FFlP38se4lWiKbDTQ%3A1672939431480&ei=pwe3Y9n5HJiW-Aa9vqWQDQ&oq=pandas+numpy+check+if+there+is+repeated+row+and+return&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAxgAMgUIIRCgATIFCCEQoAEyBQghEKABOgoIABBHENYEELADOgQIIRAVOgcIIRCgARAKSgQIQRgASgQIRhgAULDGA1i00gNg_dsDaAJwAXgAgAH1AYgB4A2SAQUwLjkuMpgBAKABAcgBCMABAQ&sclient=gws-wiz-serp
def lottopredict(amount, randomDigitOption, digitcounts):
    returnLottoArray = []
    lottoNumPredict = []
    sampleSize = 7
    lottoPlaceCount = 0

    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "../DataCollection/frequencyData.json")
    jsonfile = open(file_path, 'r')
    data = json.load(jsonfile)
    
    if int(randomDigitOption) == 0:
        for i in range(int(amount)):

            while lottoPlaceCount < sampleSize:
                r = random.randint(0,45)
                if r not in lottoNumPredict:
                    lottoPlaceCount += 1
                    lottoNumPredict.append(r)

            returnLottoArray.append(lottoNumPredict)
            lottoNumPredict = []
            lottoPlaceCount = 0

    elif int(randomDigitOption) == 1:
        digitcounts = ast.literal_eval(digitcounts)
        NumContainer = []
        tempNumContainer = []

        for nums in range(len(digitcounts)):
            for digit in range(int(digitcounts[nums])):
                if nums == 0:
                    tempNumContainer.append(data["freqeuncy"]["Num1"][digit][0])
                elif nums == 1:
                    tempNumContainer.append(data["freqeuncy"]["Num2"][digit][0])
                elif nums == 2:
                    tempNumContainer.append(data["freqeuncy"]["Num3"][digit][0])
                elif nums == 3:
                    tempNumContainer.append(data["freqeuncy"]["Num4"][digit][0])
                elif nums == 4:
                    tempNumContainer.append(data["freqeuncy"]["Num5"][digit][0])
                elif nums == 5:
                    tempNumContainer.append(data["freqeuncy"]["Num6"][digit][0])
                elif nums == 6:
                    tempNumContainer.append(data["freqeuncy"]["bnsNum"][digit][0])
            NumContainer.append(tempNumContainer)
            tempNumContainer = []
        
        j = 0
        #최소 최고 반복 숫자 조건 7, 6부터는 오류가 뜸
        for i in range(int(amount)):
            while lottoPlaceCount < sampleSize:
                tempIndex = random.randint(0, len(NumContainer[j])-1)
                r = int(NumContainer[j][tempIndex])
                if r not in lottoNumPredict:
                    lottoPlaceCount += 1
                    lottoNumPredict.append(r)

            j += 1

            returnLottoArray.append(lottoNumPredict)
            lottoNumPredict = []
            lottoPlaceCount = 0

    #결과값
    returnLotto = {
        "lottoPredict" : returnLottoArray,
        "amount" : amount
    }
    print(returnLotto)




if __name__ == '__main__':
    if sys.argv[1] == "loadLottoResultAllTime":
        loadLottoResultAllTime()
    elif sys.argv[1] == "createLottoResultAllTime":
        createLottoResultAllTime()
    elif sys.argv[1] == "LottoResultAllTimeDownload":
        LottoResultAllTimeDownload()
    elif sys.argv[1] == "checkifrepeated":
        checkifrepeated()
    elif sys.argv[1] == "createPieChart":
        createPieChart(sys.argv[2])
    elif sys.argv[1] == "lottopredict":
        lottopredict(sys.argv[2], sys.argv[3], sys.argv[4])