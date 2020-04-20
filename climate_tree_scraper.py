import time
from datetime import datetime
from googlesearch import search
from webpreview import web_preview
import warnings
import sys
import random
import json
import csv
import os
from urllib.error import HTTPError
from urllib.error import URLError

def parsePlaceCSV(filename):
    with open(filename, mode='r', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        result = []
        for row in reader:
            result.append([row['place'], row['id']])
    return result


def parseSolutionCSV():
    with open('strategy_sector_solution.csv', mode='r', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        result = []
        for row in reader:
            result.append([row['Strategy'], row['Sector'], row['Solution']])
    return result


def writeToJson(obj, placeid, num):
    with open('./output/' + placeid + "_" + str(num) + ".json", "w+", encoding='utf-8') as f:
        json.dump(obj, f)


def getJson(place_name, place_id, link, strategy, sector, solution):
    data = {}
    data['user_id'] = 0
    data['hyperlink'] = link
    if "pdf" in link:
        title = place_name + " " + solution
        desc = ""
    else:
        title, desc, image = web_preview(link, timeout=10)
    data['story_title'] = title
    data['description'] = desc
    data['rating'] = 0
    data['place_ids'] = [place_id]
    data['media_type'] = 'article'
    data['date'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    data['solution'] = [solution]
    data['sector'] = [sector]
    data['strategy'] = [strategy]
    data['comments'] = []
    data['liked_by_users'] = []
    data['flagged_by_users'] = []
    return data

warnings.filterwarnings("ignore")

if len(sys.argv) != 2:
    print("Usage: python Climate_tree_scraper.py your_csv.csv (csv must have headers: place,id)")
    sys.exit(1)

filename = sys.argv[1]
places = parsePlaceCSV(filename)
solutions = parseSolutionCSV()
if not os.path.exists('./output'):
    os.makedirs('output')
for place in places:
    num = 0
    print(place, flush=True)
    placeName = place[0]
    if not placeName:
        continue
    placeid = place[1]
    for sol in solutions:
        solutionName = sol[2]
        query = "\"" + placeName + "\"" + " climate change " + solutionName
        try:
            for link in search(query, num=1, stop=1):
                print(link, flush=True)
                tmpJson = []
                num += 1
                try:
                    tmpJson.append(getJson(placeName, placeid, link, sol[0], sol[1], solutionName))
                    writeToJson(tmpJson, placeid, num)
                except:
                    print("Preview Error: ", num, sys.exc_info()[0])
                time.sleep(3)
        except URLError as e:
            print("URLError" + str(e.reason))
        except HTTPError as e:
            print("HTTPError" + str(e.code) + str(e.reason))
        except:
            print("Search Error: ", sys.exc_info()[0])