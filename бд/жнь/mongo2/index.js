const fs = require("fs")
const { MongoClient } = require("mongodb")
const port = 1337
const client = new MongoClient("mongodb://127.0.0.1:27017/lab_mongodb")
let db
let collection

const s1 = async (category) => (await (await collection.aggregate([{$match: {category: category}}, {$group: {_id: {name: "$name"}}}])).toArray()).map(el => el._id)
const s2 = async (category) => (await (await collection.aggregate([{$match: {category: category}}, {$group: {_id: {characteristics: "$characteristics"}}}])).toArray()).map(el => el._id)
const s3 = async (customer) => (await (await collection.aggregate([{$match: {"sales.customer": customer}}, {$group: {_id: {price: "$price", name: "$name"}}}])).toArray()).map(el => el._id)
const s4 = async (color)    => (await (await collection.aggregate([{$match: {color: color}}, {$group: {_id: {manufacturer: "$manufacturer", name: "$name", price: "$price"}}}])).toArray()).map(el => el._id)
const s5 = async ()         => (await (await collection.aggregate([{$group: {_id: "$name", count: {$sum: {$size: "$sales"}}}}])).toArray()).reduce((sum, el) => sum + el.count, 0)
const s6 = async ()         => (await (await collection.aggregate([{$group: {_id: "$category", count: {$sum: 1}}}])).toArray()).map(el => {return {category: el._id, count: el.count}})
const s7 = async (product)  => (await (await collection.aggregate([{$match: {name: product}}, {$unwind: "$sales"}, {$group: {_id: {customer: "$sales.customer"}}}])).toArray()).map(el => el._id)
const s8 = async (pr, del)  => (await (await collection.aggregate([{$match: {name: pr}}, {$unwind: "$sales"}, {$match: {"sales.delivery": del}}, {$group: {_id: {customer: "$sales.customer"}}}])).toArray()).map(el => el._id)

async function main() {
    await client.connect()
    db = client.db("mongo2")

    collection = await db.collection("products")

    const k = await s8("Exam 3", "Disloyal Skin")
    console.log(k)
}
main()