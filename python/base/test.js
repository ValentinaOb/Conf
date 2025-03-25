const http = require('http');

const host = 'localhost';
const port = 3600;


const split2 = require('split2');
const through2 = require('through2');
const fs = require('fs');

const server = http.createServer((req, res) => {
    const title = [];
    let n = 0;
    const list = [];
    
    fs.createReadStream('1.csv')
        .pipe(split2())
        .pipe(through2.obj(function (chunk, enc, callback) {
            n = n + 1;
            if(n == 1){
              const row1 = chunk.split(",");
              row1.forEach((value,index)=>
                title.push(row1[index])
              )
            } else {
                let obj = {};
                let row = chunk.split(",");
                title.forEach((column, index)=>
                    obj[column]=row[index]
                )
                this.push(obj);
            }
             
            callback();
        })).on('data', (data) => {
            list.push(data)
          })
          .on('end', () => {
            res.writeHead(200);
            res.end(JSON.stringify(list));
          });
});

server.listen(port, host, () => {
    console.log("Server is running on http://${host}:${port}");
});