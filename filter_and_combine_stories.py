from os import listdir, makedirs
from os.path import isfile, join, exists
import json
import bson
import csv

# This program aggregates all of the Json story files emitted by Climate_tree_scraper.py into a single
# JSON file without duplicate links. If duplicates are found the place_id, solution, sector, and strategy
# are combined into a JSON array. If stories with no title are found one is constructed out of the place name
# and solution.

# location of input stories from the scraper
jsonDir = './output/'
# location to put output (assumed to exist)
outDir = './filtered_stories/'
# dict to build final json string
urlDict = {}

def parsePlaceCSV(filename):
    with open(filename, mode='r', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        result = {}
        for row in reader:
            result[row['id']] = row['place']
        return result

def getFiles(path):
    return [f for f in listdir(path) if isfile(join(path, f))]

def getJson(path):
    with open(path) as data:
        return json.load(data)

def addToUrlDict(story, placeIdToNameDict):
    story["posted_by"] = "ClimateTree"
    if story["hyperlink"] not in urlDict: # if we havent seen link yet add the whole story
        if story["story_title"] is None:
            story["story_title"] = placeIdToNameDict[story["place_ids"][0]] + story["solution"][0]
        urlDict[story["hyperlink"]] = story
    else:
        # if link exists already combine it with indexed story
        placeId = story["place_ids"]
        strategy = story["strategy"]
        sector = story["sector"]
        solution = story["solution"]
        urlDict[story["hyperlink"]]["place_ids"] = list(set().union(placeId,urlDict[story["hyperlink"]]["place_ids"]))
        urlDict[story["hyperlink"]]["strategy"] = list(set().union(strategy, urlDict[story["hyperlink"]]["strategy"]))
        urlDict[story["hyperlink"]]["sector"] = list(set().union(sector, urlDict[story["hyperlink"]]["sector"]))
        urlDict[story["hyperlink"]]["solution"] = list(set().union(solution, urlDict[story["hyperlink"]]["solution"]))

def writeToJson(obj):
    with open(outDir + "stories.json", "w+", encoding='utf-8') as f:
        json.dump(obj, f)

def main():
    if not exists(outDir):
        makedirs('filtered_stories')
    finalJson = []
    placeIdToNameDict = parsePlaceCSV("place_name_id.csv")
    files = getFiles(jsonDir)
    for file in files:
        addToUrlDict(getJson(jsonDir+file)[0], placeIdToNameDict)
    for key in urlDict:
        finalJson.append(urlDict[key])
    for data in finalJson:
        tmp = [int(i) for i in data["place_ids"]] #Convert string placeids to int
        data["place_ids"] = tmp
    writeToJson(finalJson)
main()