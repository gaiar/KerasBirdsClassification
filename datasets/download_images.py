from google_images_download import google_images_download
import random 
import csv

arguments = dict()
arguments["limit"] = 5
arguments["print_urls"] = False
arguments["format"] = "jpg"
arguments["size"] = ">400*300"
arguments["color_type"] = "full-color"
arguments["output_directory"] = "data"
#arguments["suffix_keywords"] = "winter,sommer,wald"
arguments["language"] = "German"
#arguments["usage_rights"] = "labeled-for-reuse"

proxies_file = open("proxies.lst", "r+")

proxies = proxies_file.readlines()
# print (random.choice(proxies))

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
        response.download(arguments)