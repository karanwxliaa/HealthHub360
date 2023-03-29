//jshint eversion:6

const fs = require('fs');
const express = require("express");
const bodyparser = require("body-parser");

const app = express();


app.use(bodyparser.json({limit:'50mb'}));
app.use(bodyparser.urlencoded({ limit: '50mb', extended: true }));
app.use(express.static("public"));
//app.use(upload())
app.set('view engine', 'ejs');
app.get("/", function (req, res) {
  res.render("index");
});


app.get("/readtest", function (req, res) {
  res.render('readtest')
});


app.get('/test', (req, res) => {
  res.render('test');
});
const atob = require('atob');

app.get('/test1', (req, res) => {
  res.render('test1');
});

  app.post('/test', async (req, res) => {
    try {
      // Parse the user's message from the request body
      const audioData = req.body.audio_data;
      const paragraph=req.body.para;
      const duration=req.body.dura;

      console.log(paragraph);
      console.log(duration);
      // create a JSON object with the data
      const data = {
        "basestr": audioData,
        "original": paragraph,
        "duration": duration
      };
  
      // Fetch responses from the JSON API
      const response = await fetch('created-api-url', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { 'Content-Type': 'application/json' },
      });
      
      // Parse the JSON response
      const json = await response.json();
      //const Pdata = json;
      res.render('test1', {data: json});
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Internal server error' });
    }
  });



let port = process.env.PORT;
if (port == null || port == "") {
  port = 3000;
}

app.listen(port, function () {
  console.log("Server started on port successfully");
});










