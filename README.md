## Climate Tree Story Scraper

This repository contains scripts that collect, process, and upload stories about climate change to the stories microservice. It depends on two csv files, one determines the places that will be searched, they are provided in the "/split_place_name_id_csvs" folder, and one "strategy_sector_soluion.csv" that contains the 205 climate change solutions that drive the scraper.

##### Before starting:

This script depends on the following (install before running):

Python 3  

External Libraries: google, webpreview, bson, pymongo

```sh
pip install google

pip install webpreview

pip install bson

pip install pymongo
```

##### Usage -- Collecting Stories:

```sh
python Climate_tree_scraper.py your_csv.csv
```

Input csv must have header place,id, as supplied by the "/split_place_name_id_csvs" folder

Output files will named placeid_storynumber.json in the created output folder. Expect about 5 seconds of runtime per story.

##### Usage -- Processing and Posting Stories:

```sh
python filter_and_combine_stories.py
```

This filters out bad stories and combines duplicates, placing them in the /filtered_stories folder that will be created if it doesn't exist.  Once it is done run upload_stories.py, see note about database connection.

```sh
python upload_stories.py
```

This posts each story in the stories.json file output by filter_and_combine_stories.py

##### Input Data:

Each file contains 50 rows and is named place_name_id_n.csv where n indicates the file number, lower numbers correspond to more populous places. 

To contribute, sign up for a input file in the class google drive folder ASD - Spring 2020/Data/Story Scraper/Story Scraper File Tracker 

Then download the corresponding file from  ASD - Spring 2020/Data/Story Scraper/Input Files and use it to run the script.

##### Database Connection:

The database URL has been removed for security reasons, update it at the top of upload_stories.py to connect to your database before uploading stories or the upload will fail. 









