from pymongo.errors import ServerSelectionTimeoutError
import datetime
import pymongo
import yaml
import os

## OPEN CONFIG FILE YAML
filename_config = os.path.abspath("Config/config.yml")
config = yaml.load(open(filename_config, "r"))

##SET DATETIME
now = datetime.date.today()

##CLASS DATABASE
class Database():
    ## fungsi untuk menginisialisasi default dalam class Database
    def __init__(self):
        self.host = config['database']['mongo']['host']
        self.database = config['database']['mongo']['database']
        self.collection = config['database']['mongo']['collection']
        self.before = config['database']['mongo']['before']
        self.port = config['database']['mongo']['port']
        self.config = config
        self.day = now.day
        self.month = now.month
        self.year = now.year

    ## fungsi untuk mengecek koneksi mongoDB
    def test_connection(self):
        client = pymongo.MongoClient("mongodb://{}:{}".format(self.host, self.port), serverSelectionTimeoutMS=10, connectTimeoutMS=20000)

        try:
            print(client.server_info())
        except ServerSelectionTimeoutError:
            print("Server is down.")

    ## fungsi untuk menginput/menginsert data ke mongoDB
    def insertData(self, database=None, collection=None, attr=None):
        myClient = pymongo.MongoClient("mongodb://{}:{}".format(self.host, self.port))
        myDB = myClient["{}".format(database)]
        myCollection = myDB["{}".format(collection)]

        try:
            myCollection.insert_many(attr)
            print('Insert Data into MongoDB Successfully')
        except:
            print('Insert Data into Mongod Failed')

    ## fungsi untuk mengambil data dari MongoDB
    def get_data(self, database=None, collection=None, source=None):
        myClient = pymongo.MongoClient("mongodb://{}:{}".format(self.host, self.port))
        myDB = myClient["{}".format(database)]
        myCollection = myDB["{}".format(collection)]

        if self.month <= 9:
            if self.day <= 9:
                iQuery = myCollection.find({
                    'publishedAt': '0{}-0{}-{}'.format(self.day, self.month, self.year),
                    'source' : source
                })
            else:
                iQuery = myCollection.find({
                    'publishedAt': '{}-0{}-{}'.format(self.day, self.month, self.year),
                    'source': source
                })
        else:
            if self.day <= 9:
                iQuery = myCollection.find({
                    'publishedAt': '0{}-{}-{}'.format(self.day, self.month, self.year),
                    'source': source
                })
            else:
                iQuery = myCollection.find({
                    'publishedAt': '{}-{}-{}'.format(self.day, self.month, self.year),
                    'source': source
                })

        return iQuery
    
    ## fungsi untuk mengambil data dari MongoDB (v2)
    def getData(self, database=None, collection=None, source=None, day=None, month=None, year=None):
        myClient = pymongo.MongoClient("mongodb://{}:{}".format(self.host, self.port))
        myDB = myClient["{}".format(database)]
        myCollection = myDB["{}".format(collection)]

        if month <= 9:
            if day <= 9:
                iQuery = myCollection.find({
                    'publishedAt': '0{}-0{}-{}'.format(day, month, year),
                    'source' : source
                })
            else:
                iQuery = myCollection.find({
                    'publishedAt': '{}-0{}-{}'.format(day, month, year),
                    'source': source
                })
        else:
            if day <= 9:
                iQuery = myCollection.find({
                    'publishedAt': '0{}-{}-{}'.format(day, month, year),
                    'source': source
                })
            else:
                iQuery = myCollection.find({
                    'publishedAt': '{}-{}-{}'.format(day, month, year),
                    'source': source
                })

        return iQuery

    ## fungsi ini digunakan untuk menghapus data harian berdasarkan sourcenya
    def delete_dataDaily(self, database=None, collection=None, source=None):
        myClient = pymongo.MongoClient("mongodb://{}:{}".format(self.host, self.port))
        myDB = myClient["{}".format(database)]
        myCollection = myDB["{}".format(collection)]

        if self.month <= 9:
            if self.day <= 9:
                iQuery = myCollection.remove({
                    'publishedAt': '0{}-0{}-{}'.format(self.day, self.month, self.year),
                    'source' : source
                })
            else:
                iQuery = myCollection.remove({
                    'publishedAt': '{}-0{}-{}'.format(self.day, self.month, self.year),
                    'source': source
                })
        else:
            if self.day <= 9:
                iQuery = myCollection.remove({
                    'publishedAt': '0{}-{}-{}'.format(self.day, self.month, self.year),
                    'source': source
                })
            else:
                iQuery = myCollection.remove({
                    'publishedAt': '{}-{}-{}'.format(self.day, self.month, self.year),
                    'source': source
                })

        return iQuery

    ## fungsi delete monthly
    def deleteMonthly(self, database=None, collection=None, source=None, day=None, month=None, year=None):
        myClient = pymongo.MongoClient("mongodb://{}:{}".format(self.host, self.port))
        myDB = myClient["{}".format(database)]
        myCollection = myDB["{}".format(collection)]

        if month <= 9:
            if day <= 9:
                iQuery = myCollection.remove({
                    'publishedAt': '0{}-0{}-{}'.format(day, month, year),
                    'source' : source
                })
            else:
                iQuery = myCollection.remove({
                    'publishedAt': '{}-0{}-{}'.format(day, month, year),
                    'source': source
                })
        else:
            if day <= 9:
                iQuery = myCollection.remove({
                    'publishedAt': '0{}-{}-{}'.format(day, month, year),
                    'source': source
                })
            else:
                iQuery = myCollection.remove({
                    'publishedAt': '{}-{}-{}'.format(day, month, year),
                    'source': source
                })

        return iQuery

    def deleteDataMonthly(self, database=None, collection=None, source=None, month=None, year=None):
        myClient = pymongo.MongoClient("mongodb://{}:{}".format(self.host, self.port))
        myDB = myClient["{}".format(database)]
        myCollection = myDB["{}".format(collection)]

        iQuery = myCollection.deleteMany({
            'source' : source,
            'publishedAt': {
                '$gte': '01-{}-{}'.format(month, year),
                '$lte': '31-{}-{}'.format(month, year)
            }
        })

        return iQuery

    ## fungsi ini digunakan untuk menghapus rss tempo di collection iBefore
    def deleteRssBefore(self, database=None, collection=None, source=None, day=None, month=None, year=None):
        myClient = pymongo.MongoClient("mongodb://{}:{}".format(self.host, self.port))
        myDB = myClient["{}".format(database)]
        myCollection = myDB["{}".format(collection)]

        if self.month <= 9:
            if self.day <= 9:
                iQuery = myCollection.remove({
                    'publishedAt': '0{}-0{}-{}'.format(self.day, self.month, self.year),
                    'source' : source
                })
            else:
                iQuery = myCollection.remove({
                    'publishedAt': '{}-0{}-{}'.format(self.day, self.month, self.year),
                    'source': source
                })
        else:
            if self.day <= 9:
                iQuery = myCollection.remove({
                    'publishedAt': '0{}-{}-{}'.format(self.day, self.month, self.year),
                    'source': source
                })
            else:
                iQuery = myCollection.remove({
                    'publishedAt': '{}-{}-{}'.format(self.day, self.month, self.year),
                    'source': source
                })

        return iQuery

    ## fungsi untuk menginput/menginsert data ke mongoDB
    def singleInsert(self, database=None, collection=None, attr=None):
        myClient = pymongo.MongoClient("mongodb://{}:{}".format(self.host, self.port))
        myDB = myClient["{}".format(database)]
        myCollection = myDB["{}".format(collection)]

        try:
            myCollection.insert(attr)
            print('Insert Data into MongoDB Successfully')
        except:
            print('Insert Data into Mongod Failed')

    ## fungsi ini digunakan untuk mengambil data
    def getDataset(self, database=None, collection=None, category=None):
        myClient = pymongo.MongoClient("mongodb://{}:{}".format(self.host, self.port))
        myDB = myClient["{}".format(database)]
        myCollection = myDB["{}".format(collection)]

        iData = []
        iQuery = collection.find(
            {"category": "{}".format(category)}, 
            {
                "category": 1, 
                "title": 1,
                "url": 1,
                "cleanContent": 1
            })
        
        for query in iQuery: iData.append(query)
            
        return iData
    
    ## fungsi ini digunakan untuk mengambil data di collection iBefore
    def getDataBefore(self, database=None, collection=None):
        myClient = pymongo.MongoClient("mongodb://{}:{}".format(self.host, self.port))
        myDB = myClient["{}".format(database)]
        myCollection = myDB["{}".format(collection)]

        iData = []

        if self.month <= 9:
            if self.day <= 9:
                iQuery = myCollection.find({
                    'publishedAt': '0{}-0{}-{}'.format(self.day, self.month, self.year)
                })
            else:
                iQuery = myCollection.find({
                    'publishedAt': '{}-0{}-{}'.format(self.day, self.month, self.year)
                })
        else:
            if self.day <= 9:
                iQuery = myCollection.find({
                    'publishedAt': '0{}-{}-{}'.format(self.day, self.month, self.year)
                }).limit(2)
            else:
                iQuery = myCollection.find({
                    'publishedAt': '{}-{}-{}'.format(self.day, self.month, self.year)
                })

        for query in iQuery: iData.append(query)

        return iData

    
