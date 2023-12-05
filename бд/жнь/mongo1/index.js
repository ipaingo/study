const express = require("express")
const bodyParser = require('body-parser')
const fs = require("fs")
const { MongoClient } = require("mongodb")
const app = express()
app.use(bodyParser.json())
const port = 1337
const client = new MongoClient("mongodb://127.0.0.1:27017/lab_mongodb")
let db

const document_input_html = fs.readFileSync("index_input.html").toString()
const document_filter_html = fs.readFileSync("index_filter.html").toString()
const document_aggregate_html = fs.readFileSync("index_aggregate.html").toString()

app.get("/", async (req, res) => {
    res.redirect("/add_document_menu")
})

app.get("/add_document_menu", async (req, res) => {
    res.send(document_input_html)
})

app.get("/filter_document_menu", async (req, res) => {
    res.send(document_filter_html)
})

app.get("/aggregate_document_menu", async (req, res) => {
    res.send(document_aggregate_html)
})

app.post("/save_document", async (req, res) => {
    let collection = await db.collection(req.body.collection)
    collection.insertOne(req.body.document)

    res.sendStatus(204)
})

app.get("/get_documents", async (req, res) => {
    let collection = await db.collection(req.query.collection)
    let docs = []
    let compares = {}
    if (req.query.key) {
        compares = {}
        compares[req.query.key] = {}
        compares[req.query.key][`$${req.query.compare}`] = req.query.value
    }
    for await (let doc of await collection.find(compares)) {
        delete doc._id
        docs.push(doc)
    }
    // console.log(docs)

    res.send({documents: docs})
})

app.post("/query_documents", async (req, res) => {
    let collection = await db.collection(req.query.collection)
    let query = []
    console.log(req.body)
    for (const key in req.body) {
        let q = {}
        q[key] = req.body[key]
        query.push(q)
    }

    console.log(query)

    let docs = []
    try {
        for await (let doc of await collection.aggregate(query)) {
            docs.push(doc)
        }
    } catch (err) {
        console.log(err)
        res.send({error: err})
        return
    }

    console.log(docs)

    res.send({documents: docs})
})


app.listen(port, async () => {
    console.log(`ОК ${port}`)

    await client.connect()
    db = client.db("mongo1")
})