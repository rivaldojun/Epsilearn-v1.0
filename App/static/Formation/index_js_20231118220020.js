
const express = require("express");
const bodyParser = require("body-parser");
const mysql = require("mysql");
const cors = require("cors");
const cron = require('cron');
const path = require("path");
//import controllers
const { createArticle } = require("./controllers/article.controller");
const {generateText} = require("./controllers/openai.controller");
const {generateImg} = require("./controllers/text2image");
const { generate_text,article_getAll , article_create ,article_update ,article_delete }= require("./controllers/data_handle")

// Constants
const PORT = process.env.PORT || 8090;
const HOST = "localhost";
const openAiKey = "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"

// App
const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cors({origin: true,methods: ["GET", "POST", "PUT", "DELETE"],credentials: true,}));
// Définir EJS comme moteur de modèle
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
// Make sure you place body-parser before your CRUD handlers!
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested-With, Content, Accept, Content-Type, Authorization"
  );
  res.setHeader(
    "Access-Control-Allow-Methods",
    "GET, POST, PUT, DELETE, PATCH, OPTIONS"
  );
  next();
});
app.use(express.json());
app.use(express.static('./ressources/assets'))
app.use(express.urlencoded({ extended: true }));

// app.get("/generate", (req, res) => {
//   res.sendFile(__dirname + "/public/generate.html");
// });

//generate dallee img
// generateImg('des usines qui poluent' , openAiKey , 1)

const create_funny = async(req,res) => {
  // console.log(req.body.prompt);
  let prompt = req.body.prompt
  generateImg(prompt, openAiKey , 1).then((response)=>{
    console.log(response);
    req.image = response
    generateText(prompt).then(
      (response)=>{
        console.log("text");
        console.log(response);
        createArticle(prompt,response,req.image ).then(()=>{
         res.status(201).json("success !");
         return "success" 
        })
      }
    );
  })
}


generateImg("La pollution est un problème mondial qui menace la santé et l'environnement. Nous devons tous prendre des mesures pour réduire notre empreinte écologique et protéger notre planète pour les générations futures." , 1)
// create_funny ({prompt : "hello !"})
//Routes
/******/
app.get("/articles/:id", article_getAll);

app.post("/articles", article_create);

app.post("/search", create_funny);


app.put("/articles/:id", article_update);

app.delete("/articles/:id", article_delete);

app.post("/generate", generate_text,generateImg);
app.get("/generate", (req, res) => {
  res.render("generate", { conversations: [] }); // Passer un tableau vide pour les conversations
});



/******/


app.listen(PORT, HOST, () => {
  console.log(`Running on http://${HOST}:${PORT}`);
});

// cron 

// job_theme.start();