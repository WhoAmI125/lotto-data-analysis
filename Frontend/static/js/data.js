window.onload = function(){
    getDataForEachNum()
    loaddefaultPieChart()

    document.getElementById("btn_create").addEventListener("click", createPieChart);
    document.getElementById("downloadAllRecord").addEventListener("click", downloadAllRecord);
    document.getElementById("downloadmostcommon").addEventListener("click", downloadmostcommon);
}

async function getDataForEachNum() {
    let loadLottoResultAllTime = await fetch("/getDataForEachNum", {
          method: 'GET',
    })
    .then(response => response.json())
    .catch(err => console.error(err))
    
    var title = document.getElementById('title');
    var thead = document.getElementById('dataHead');
    var tbody = document.getElementById('dataBody');
    datasetNum = loadLottoResultAllTime["datasetNum"]
    loadLottoResultAllTime = loadLottoResultAllTime["freqeuncy"]

    title.innerHTML += "로또 번호 자리 - 가장 많이 나온 숫자";

    var insertTr = "";
    insertTr += "<th>" + '첫번째 자리' + "</th>";
    insertTr += "<th>" + '두번째 자리' + "</th>";
    insertTr += "<th>" + '세번째 자리' + "</th>";
    insertTr += "<th>" + '네번째 자리' + "</th>";
    insertTr += "<th>" + '다섯번째 자리' + "</th>";
    insertTr += "<th>" + '여섯번째 자리' + "</th>";
    insertTr += "<th>" + "보너스 숫자" + "</th>";
    thead.innerHTML += insertTr;

    for (var i = 0; i < 10; i++) 
    {
        var insertTr = "";

        insertTr += "<tr>";
        insertTr += "<td>" + String(loadLottoResultAllTime['Num1'][i][0]) + " (" + String((100*loadLottoResultAllTime['Num1'][i][1]/datasetNum).toFixed(2)) +"%) </td>";
        insertTr += "<td>" + String(loadLottoResultAllTime['Num2'][i][0]) + " (" + String((100*loadLottoResultAllTime['Num2'][i][1]/datasetNum).toFixed(2)) +"%) </td>";
        insertTr += "<td>" + String(loadLottoResultAllTime['Num3'][i][0]) + " (" + String((100*loadLottoResultAllTime['Num3'][i][1]/datasetNum).toFixed(2)) +"%) </td>";
        insertTr += "<td>" + String(loadLottoResultAllTime['Num4'][i][0]) + " (" + String((100*loadLottoResultAllTime['Num4'][i][1]/datasetNum).toFixed(2)) +"%) </td>";
        insertTr += "<td>" + String(loadLottoResultAllTime['Num5'][i][0]) + " (" + String((100*loadLottoResultAllTime['Num5'][i][1]/datasetNum).toFixed(2)) +"%) </td>";
        insertTr += "<td>" + String(loadLottoResultAllTime['Num6'][i][0]) + " (" + String((100*loadLottoResultAllTime['Num6'][i][1]/datasetNum).toFixed(2)) +"%) </td>";
        insertTr += "<td>" + String(loadLottoResultAllTime['bnsNum'][i][0]) + " (" + String((100*parseFloat(loadLottoResultAllTime['bnsNum'][i][1])/datasetNum).toFixed(2)) +"%) </td>";
        insertTr += "</tr>";
        tbody.innerHTML += insertTr;
    }
    
}

async function loaddefaultPieChart() {
    let defaultPieChart = await fetch("/data/defaultPieChart", {
        method: 'GET',
    })
    .then(response => response.blob())
    .then(imageBlob => {
            // Then create a local URL for that image and print it 
            const imageObjectURL = URL.createObjectURL(imageBlob);
            console.log(imageObjectURL);

            const image = document.createElement('img')
            image.src = imageObjectURL
            image.style.width = "600px"
            image.style.height = "450px"
            image.style.objectFit = "cover"

            const container = document.getElementById("piechart")
            container.insertBefore(image, container.firstChild);
            
    })
    .catch(err => console.error(err));
}

async function createPieChart() {
    let e = document.getElementById("piechartform");
    let value = e.value;
    let data = {
        "name": "wantedPieChartNum",
        "value": value,
    }

    console.log(data)

    let response = await fetch("/data/createPieChart",{
    "method": "POST",
    "headers": {"Content-Type": "application/json"},
    "body": JSON.stringify(data),
    })
    .then(response => response.blob())
    .then(imageBlob => {
            // Then create a local URL for that image and print it 
            const imageObjectURL = URL.createObjectURL(imageBlob);
            console.log(imageObjectURL);

            const image = document.createElement('img')
            image.src = imageObjectURL
            image.style.width = "600px"
            image.style.height = "450px"
            image.style.objectFit = "cover"
            const container = document.getElementById("piechart")
            container.removeChild(container.firstElementChild);
            container.insertBefore(image, container.firstChild);
            
    })
    .catch(err => console.error(err));
}

async function downloadAllRecord() {
    let resposne = await fetch("/data/downloadAllRecord",{
        "method": "GET",
    })
    window.open(resposne.url);
}

async function downloadmostcommon() {
    let resposne = await fetch("/data/downloadmostcommon",{
        "method": "GET",
    })
    window.open(resposne.url);
}