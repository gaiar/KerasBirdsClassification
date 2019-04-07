import requests
import re
from google_images_download import google_images_download
import random
import csv
import os
import sys
import logging


logging.basicConfig(
    filename='downloader.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

DOWNLOAD_FOLDER = "data-clean"

STOP_WORDS = ""
STOP_WORDS_SHUFFLE = False
DOWNLOAD_VALIDATION = True
USE_FINETUNING = True
USE_FINETUNING_EXTRA = False



def prepare_proxies():
    try:
        with open('proxies.lst', newline='') as proxies:
            pl = proxies.read().splitlines()
            if len(pl) > 1:
                return pl
    except Exception as err:
        logging.error("Problem opening proxies file. {0}".format(err))
        return None


def prepare_stop_words():
    try:
        with open('stop-words', newline='') as stopwords:
            sw = stopwords.read().splitlines()
            if STOP_WORDS_SHUFFLE:
                random.shuffle(sw)
            sw = sw[:29]
            words = ' -'.join([str(x) for x in sw])
            words = "-" + words
        return words
    except Exception as err:
        logging.error("Problem opening stop-words file. {0}".format(err))
        return None


STOP_WORDS = prepare_stop_words()
PROXIES = prepare_proxies()
PROXIES = None

if STOP_WORDS is None:
    print("[ERROR] :: Please check stop-words file")
    sys.exit()


logging.debug("STOP WORDS to be used {0}".format(STOP_WORDS))
logging.debug("PROXIES to be used {0}".format(PROXIES))


PROXIES = None


def download_from_google():
    # Prepare config for google_images_download
    arguments = dict()
    arguments["limit"] = 1000
    arguments["print_urls"] = False
    arguments["format"] = "jpg"
    arguments["size"] = ">400*300"
    arguments["color_type"] = "full-color"
    arguments["output_directory"] = DOWNLOAD_FOLDER
    arguments["chromedriver"] = "/Users/user/Developer/conda-stuff/birds-of-berlin/datasets/chromedriver"
    #arguments["chromedriver"] = "/home/gaiar/developer/smart-birds-feeder/datasets/chromedriver"

    # Extra fine-tuning if needed
    if USE_FINETUNING:
        arguments["suffix_keywords"] = "winter,sommer,wald"

    if USE_FINETUNING_EXTRA:
        arguments["language"] = "German"
        arguments["usage_rights"] = "labeled-for-reuse"

    with open('berlin-birds-extended.csv', newline='') as csvfile:
        birdreader = csv.DictReader(csvfile, delimiter=',')
        for row in birdreader:
            response = google_images_download.googleimagesdownload()
            if len(row["alt_name"]) > 1:
                keywords = "{0} OR {1} OR {2} {3}".format(
                    row["name"], row["alt_name"], row["latin_name"], STOP_WORDS)
            else:
                keywords = "{0} OR {1} {2}".format(
                    row["name"], row["latin_name"], STOP_WORDS)

            arguments["keywords"] = keywords
            prefix = "{0}{1}".format(
                row["name"].lower().replace(" ", "_"), "_")
            arguments["prefix"] = prefix
            arguments["image_directory"] = row["name"]

            if PROXIES is not None:
                arguments["proxy"] = random.choice(PROXIES).strip()
                logging.info("Using proxy {0}".format(arguments["proxy"]))

            print("Downloading {}".format(arguments))
            logging.info("Downloading {}".format(arguments))

            try:
                response.download(arguments)
            except Exception as error:
                logging.error(
                    "Problem downloading {0}. {1}".format(arguments, error))
                response.download(arguments)


DATA_DIR = "{}/test".format(DOWNLOAD_FOLDER)


def get_directory(bird_name):
    directory = os.path.join(DATA_DIR, bird_name)
    try:
        os.mkdir(directory)
    except OSError:
        print("[WARN] :: Directory {0} already exist".format(directory))
        logging.warning("Directory {0} already exist".format(directory))
    else:
        print("[INFO] :: Directory {0} created".format(directory))
        logging.info("Directory {0} created".format(directory))
    finally:
        return directory


def dowload_original_files():
    with open('berlin-birds-extended.csv', newline='') as csvfile:
        birdreader = csv.DictReader(csvfile, delimiter=',')
        for row in birdreader:
            print("[INFO] :: Downloading {0}".format(row["image_url"]))
            logging.info("Downloading {0}".format(row["image_url"]))
            try:
                r = requests.get(row["image_url"], allow_redirects=True)
                if row["image_url"].find('/'):
                    filename = row["image_url"].rsplit('/', 1)[1]
                filename = os.path.join(get_directory(row["name"]), filename)
                print("[INFO] :: Writing {0}".format(filename))
                logging.info("Writing {0}".format(filename))
                with open(filename, 'wb') as image_file:
                    image_file.write(r.content)
            except Exception as e:
                print("[ERROR] :: Problem downloading {0}. {1}".format(
                    row["image_url"], e))
                logging.error("Problem downloading {0}. {1}".format(
                    row["image_url"], e))


download_from_google()

if DOWNLOAD_VALIDATION:
    dowload_original_files()
