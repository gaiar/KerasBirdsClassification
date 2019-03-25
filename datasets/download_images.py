from google_images_download import google_images_download
import random 
import csv


def download_from_google():

    #Prepare config for google_images_download
    arguments = dict()
    arguments["limit"] = 100
    arguments["print_urls"] = False
    arguments["format"] = "jpg"
    arguments["size"] = ">400*300"
    arguments["color_type"] = "full-color"
    arguments["output_directory"] = "data"

    #Extra fine-tuning if needed
    
    #arguments["suffix_keywords"] = "winter,sommer,wald"
    #arguments["language"] = "German"
    #arguments["usage_rights"] = "labeled-for-reuse"

    #Get proxies 
    proxies_file = open("proxies.lst", "r+")
    proxies = proxies_file.readlines()

    with open('berlin-birds.csv', newline='') as csvfile:
        birdreader = csv.DictReader(csvfile, delimiter=',')
        for row in birdreader:
            # print(row[0])
            response = google_images_download.googleimagesdownload()
            keywords = "{0} OR {1} {2}".format(row["name"], row["latin_name"], "-stock")
            prefix = "{0}{1}".format(row["name"].lower().replace(" ", "_"), "_")
            arguments["keywords"] = keywords
            arguments["prefix"] = prefix
            arguments["image_directory"] = row["name"]
            arguments["proxy"] = random.choice(proxies).strip()
            print("Downloading {}".format(arguments))
            try:
                response.download(arguments)
            except Exception:
                arguments["proxy"] = random.choice(proxies).strip()
                response.download(arguments)

    proxies_file.close()

def dowload_original_files():
    with open('berlin-birds.csv', newline='') as csvfile:
        birdreader = csv.DictReader(csvfile, delimiter=',')
    