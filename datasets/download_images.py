import requests
import re
from google_images_download import google_images_download
import random
import csv
import os


def download_from_google():

    # Prepare config for google_images_download
    arguments = dict()
    arguments["limit"] = 200
    arguments["print_urls"] = False
    arguments["format"] = "jpg"
    arguments["size"] = ">400*300"
    arguments["color_type"] = "full-color"
    arguments["output_directory"] = "data"
    arguments["chromedriver"] = "/home/gaiar/developer/smart-birds-feeder/datasets/chromedriver"

    # Extra fine-tuning if needed

    #arguments["suffix_keywords"] = "winter,sommer,wald"
    arguments["language"] = "German"
    #arguments["usage_rights"] = "labeled-for-reuse"

    # Get proxies
    proxies_file = open("proxies.lst", "r+")
    proxies = proxies_file.readlines()

    with open('berlin-birds.csv', newline='') as csvfile:
        birdreader = csv.DictReader(csvfile, delimiter=',')
        for row in birdreader:
            # print(row[0])
            response = google_images_download.googleimagesdownload()
            keywords = "{0} OR {1} {2}".format(
                row["name"], row["latin_name"], "-stock -watermark")
            prefix = "{0}{1}".format(
                row["name"].lower().replace(" ", "_"), "_")
            arguments["keywords"] = keywords
            arguments["prefix"] = prefix
            arguments["image_directory"] = row["name"]
            #arguments["proxy"] = random.choice(proxies).strip()
            print("Downloading {}".format(arguments))
            try:
                response.download(arguments)
            except Exception:
                arguments["proxy"] = random.choice(proxies).strip()
                response.download(arguments)

    proxies_file.close()


def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


DATA_DIR = "data/test"


def get_directory(bird_name):
    directory = os.path.join(DATA_DIR, bird_name)
    try:
        os.mkdir(directory)
    except OSError:
        print("[WARN] :: Directory {0} already exist".format(directory))
    else:
        print("[INFO] :: Directory {0} created".format(directory))
    finally:
        return directory


def dowload_original_files():
    with open('berlin-birds.csv', newline='') as csvfile:
        birdreader = csv.DictReader(csvfile, delimiter=',')
        for row in birdreader:
            print("[INFO] :: Downloading {0}".format(row["image_url"]))
            try:
                r = requests.get(row["image_url"], allow_redirects=True)
                #filename = get_filename_from_cd(r.headers.get('content-disposition'))
                if row["image_url"].find('/'):
                    filename = row["image_url"].rsplit('/', 1)[1]
                filename = os.path.join(get_directory(row["name"]), filename)

                print("[INFO] :: Writing {0}".format(filename))
                with open(filename, 'wb') as image_file:
                    image_file.write(r.content)
            except Exception as e:
                print("[ERROR] :: Problem downloading {0}. {1}".format(
                    row["image_url"], e))


#dowload_original_files()

download_from_google()