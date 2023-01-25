const express = require("express");
const http = require("http");
const mongoose = require("mongoose") //데이터 저장을 위한 몽구스 구현
const fs = require('fs') //Node.js 내장 모듈 호출
const app = express(); //express 객체 생성
const server = http.createServer(app); //express http 서버 생성
var path = require('path'); //기본 path 위치 가지고오기
const {spawn} = require('child_process'); //python 파일 실행시키기
const schedule = require('node-schedule') //cron 기능 활호화

//웹사이트 기능
/*
- 역대 로또 기록 보여주기
- 특정 번호 위치에 가장 많이 나온 기록 보여주기
- 백테스팅 기능
*/

//토요일 오후 10시 1분 (22:01)에 로또 데이터 업데이트 코드 돌리기
schedule.scheduleJob("1 22 * * 6", () => {
    const python = spawn('python3', ['./DataCrawling/dataExtraction.py']);
    python.stdout.on('data', async function(data) {
        dataToSend = await data.toString();
        console.log(dataToSend)
    }); 
})



// Parse URL-encoded bodies (as sent by HTML forms)
app.use(express.urlencoded({
    extended: true
}));
// Parse JSON bodies (as sent by API clients)
app.use(express.json());
//css랑 js 불러오기
app.use("/css", express.static("./Frontend/static/css"))
app.use("/js", express.static("./Frontend/static/js"))



app.get('/',function(req,res) {
    console.log(__dirname)
    res.sendFile(path.join(__dirname, '../Frontend/static', 'index.html'));
});

app.get('/data',function(req,res) {
    res.sendFile(path.join(__dirname, '../Frontend/static', 'data.html'));
});

app.get('/getDataForEachNum', function(req, res) {
    //child process을 통해서 node.js에서 파이썬을 돌린다
    /*const python = spawn('python3', ['./DataCrawling/dataAnalysis.py', 'loadLottoResultAllTime']);
    python.stdout.on('data', (data) => {
        dataToSend = data.toString();
    }); 
    //결과를 인덱스로 보낸다
    python.on('close', (code) => {
        res.send(dataToSend);
    })*/
    let rawdata = fs.readFileSync(path.join(__dirname, '../DataCollection', 'frequencyData.json'));
    let dataToSend = JSON.parse(rawdata);
    //console.log(dataToSend);
    res.send(dataToSend);
});

app.get('/data/defaultPieChart', function(req, res) {
    //console.log(dataToSend);
    //console.log((path.join(__dirname, '../DataCollection', 'No1.png')))
    res.sendFile(path.join(__dirname, '../DataCollection', 'No1.png'));
});

app.get('/data/downloadAllRecord', function(req, res, next) {
    const filePath = path.join(__dirname, '../DataCollection', 'lottoResultAllTime.csv');
    console.log("download all record csv ", filePath)
    res.download(filePath);
    //res.download(__dirname + '../DataCollection/lottoResultAllTime.csv', 'lottoResultAllTime.csv');
});

app.get('/data/downloadmostcommon', async function(req, res, next) {

    const python = spawn('python3', ['./DataCrawling/dataAnalysis.py', 'LottoResultAllTimeDownload']);
    python.stdout.on('data', async function(data) {
        dataToSend = await data.toString();
        console.log(dataToSend)
    }); 

    const filePath = path.join(__dirname, '../DataCollection', 'frequencyDataDownload.json');

    console.log("download frequency of all data", filePath)
    res.download(filePath);

    //res.download(__dirname + '../DataCollection/lottoResultAllTime.csv', 'lottoResultAllTime.csv');
});

app.post('/data/createPieChart', async function(req, res) {
    console.log(req.body.value);
    if(req.body.value === "") {
        res.sendFile(path.join(__dirname, '../DataCollection', 'No1.png'));
    }

    const python = await spawn('python3', ['./DataCrawling/dataAnalysis.py', 'createPieChart',req.body.value]);
    await python.stdout.on('data', (data) => {
        dataToSend = data.toString();
        console.log(dataToSend)
    }); 

    res.sendFile(path.join(__dirname, '../DataCollection', req.body.value+'.png'));

});

//서버를 5000 포트로 listen
server.listen(5000, function() {
    console.log("Server is running")
})


