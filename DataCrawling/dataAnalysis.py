import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from collections import Counter
import os, json, sys


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
        


if __name__ == '__main__':
    if sys.argv[1] == "loadLottoResultAllTime":
        loadLottoResultAllTime()
    elif sys.argv[1] == "createLottoResultAllTime":
        createLottoResultAllTime()
    elif sys.argv[1] == "LottoResultAllTimeDownload":
        LottoResultAllTimeDownload()
    elif sys.argv[1] == "createPieChart":
        createPieChart(sys.argv[2])
