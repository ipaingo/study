const fs = require("fs")
const { MongoClient } = require("mongodb")
const port = 1337
const client = new MongoClient("mongodb://127.0.0.1:27017/lab_mongodb")

const irand = (min, max) => Math.floor(Math.random() * (max - min + 1) + min)
const rand_item = (collection) => collection[irand(0, collection.length - 1)]

async function main() {
    let db
    await client.connect()
    db = client.db("mongo2")

    let collection = await db.collection("products")
    try {
    await collection.drop()
    } catch (err) {}

    const customers_am = irand(15, 25)
    const manufacturer_am = irand(4, 7)
    const delivery_am = irand(4, 7)
    const product_category_am = 4
    const products_am = irand(25, 35)

    let customers = []
    let manufacturers = []
    let deliveries = []
    let product_categories = []
    let products = []

    const adjectives = fs.readFileSync("adjectives.txt").toString().split("\r\n")
    const nouns = fs.readFileSync("nouns.txt").toString().split("\r\n")
    const colors = fs.readFileSync("colors.txt").toString().split("\r\n")
    const firstnames = fs.readFileSync("firstnames.txt").toString().split("\r\n")
    const surnames = fs.readFileSync("surnames.txt").toString().split("\r\n")
    const home_appliannces = fs.readFileSync("home_appliances.txt").toString().split("\r\n")

    for (let i = 0; i < customers_am; i++)
        customers.push(rand_item(firstnames) + " " + rand_item(surnames))
    
    for (let i = 0; i < manufacturer_am; i++)
        manufacturers.push(rand_item(adjectives) + " " + rand_item(nouns))
    
    for (let i = 0; i < delivery_am; i++)
        deliveries.push(rand_item(adjectives) + " " + rand_item(nouns))
    
    for (let i = 0; i < product_category_am; i++)
        product_categories.push(rand_item(home_appliannces))
    
    for (let i = 0; i < products_am; i++) {
        let product = {
            name:   (irand(0, 1) ? rand_item(adjectives) + " " : "") + 
                    (irand(0, 1) ? rand_item(adjectives) + " " : "") +
                    rand_item(nouns) +
                    (irand(0, 1) ? " " + irand(1, 5) : ""),
            category: rand_item(product_categories),
            color: rand_item(colors),
            manufacturer: rand_item(manufacturers),
            characteristics:    (irand(0, 1) ? rand_item(adjectives) + ", " : "") + 
                                (irand(0, 1) ? rand_item(adjectives) + ", " : "") +
                                (irand(0, 1) ? rand_item(adjectives) + ", " : "") +
                                rand_item(adjectives),
            price: irand(1, 2000),
            sales: [],
        }

        let sales_am = irand(0, 8)
        for (let j = 0; j < sales_am; j++) {
            let sale = {
                customer: rand_item(customers),
                delivery: rand_item(deliveries),
                comment:    (irand(0, 1) ? rand_item(adjectives) + ", " : "") + 
                            (irand(0, 1) ? rand_item(adjectives) + ", " : "") +
                            rand_item(adjectives),
                rate: irand(1, 5),
            }

            product.sales.push(sale)
        }

        products.push(product)
    }

    console.log(products)
    await collection.insertMany(products)

    process.exit(0)
}
main()