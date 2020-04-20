import pymongo
from os import listdir
from os.path import isfile, join
import json
import bson

jsonDir = './filtered_stories/'
dbName = 'climateTree'
collectionName = 'story'
connStr = 'mongodb://'

def getFiles(path):
    return [f for f in listdir(path) if isfile(join(path, f))]

def insertOne(collection,data):
    if data['story_title'] is not None and len(data['story_title'])<=1000:
        data['story_id']=str(bson.ObjectId())
        collection.insert_one(data)

def getClient(path):
    return pymongo.MongoClient(path)

def getDB(client,dbName):
    return client[dbName]

def getCollection(db,collectionName):
    return db[collectionName]

def main():
    cli=getClient(connStr)
    col=getCollection(getDB(cli,dbName),collectionName)
    count=0
    for f in getFiles(jsonDir):
        with open(jsonDir+f) as file:
            for data in json.load(file): #Itereate over each object in the file (an array)
                count+=1
                if count>=10000:
                    break
                insertOne(col,data)
        print(count)
    cli.close()
main()