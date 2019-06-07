#!/usr/bin/env python
# coding: utf-8
from pyinaturalist.node_api import get_all_observations, get_observations, make_inaturalist_api_get_call
import csv
from pprint import pprint
from tempfile import NamedTemporaryFile
import shutil
import csv
import shelve
import logging
import os
import requests
from multiprocessing.pool import ThreadPool
from fake_useragent import UserAgent
import random

THROTTLING_DELAY = 0.55

logging.basicConfig(
    filename='inat_photos.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


fields = ["name","alt_name","russian_name","wiki_de","latin_name","image_url","inat_id","wiki_en","preferred_name","inat_name"]

def prepare_proxies():
    prx = []
    try:
        with open('proxylist.lst') as proxies:
            pl = proxies.read().splitlines()
            #print(pl)
            for proxy in pl:
                prx.append({"http":str(proxy), "https":str(proxy)})
    except Exception as err:
        logging.error("Problem opening proxies file. {0}".format(err))
        return None
    return prx if len(prx)>0 else None



def get_inat_taxa_id():
    birdsfile = 'berlin-birds-extended.csv'
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    with open(birdsfile, newline='',encoding='utf8') as csvfile,tempfile:
            birdreader = csv.DictReader(csvfile, delimiter=',')
            birdswriter = csv.DictWriter(tempfile, delimiter=';',fieldnames=fields)
            birdswriter.writeheader()
            for row in birdreader:
                latin_name = str(row["latin_name"]).split("/")[0]
                print("Checking {0}".format(latin_name))
                taxa = None
                try:
                    taxa = make_inaturalist_api_get_call("taxa",params={"q":row["russian_name"]}).json()["results"][0]
                except Exception:
                    taxa = make_inaturalist_api_get_call("taxa",params={"q":row["name"]}).json()["results"][0]
                
                newrow = {"name":row["name"],
                    "alt_name":row["alt_name"],
                    "russian_name":row["russian_name"],
                    "wiki_de":row["wiki_de"],
                    "latin_name":row["latin_name"],
                    "image_url":row["image_url"],
                    "inat_id":taxa["id"] if "id" in taxa else None,
                    "wiki_en":taxa["wikipedia_url"] if "wikipedia_url" in taxa else None,
                    "preferred_name":taxa["preferred_common_name"] if "preferred_common_name" in taxa else None,
                    "inat_name": taxa["name"] if "name" in taxa else None
                    }
                birdswriter.writerow(newrow)
                if taxa:
                    print("{0} matching {1}".format(latin_name, taxa["name"]))

    shutil.move(tempfile.name, "berlin-birds-extended-inat.csv")                




# Turdus merula
# {'ancestor_ids': [48460, 1, 2, 355675, 3, 7251, 15977, 12705, 12716],
#  'ancestry': '48460/1/2/355675/3/7251/15977/12705',
#  'atlas_id': None,
#  'complete_rank': 'subspecies',
#  'complete_species_count': None,
#  'current_synonymous_taxon_ids': None,
#  'default_photo': {'attribution': '(c) Ashley M Bradford, some rights reserved '
#                                   '(CC BY-NC)',
#                    'flags': [],
#                    'id': 7885442,
#                    'license_code': 'cc-by-nc',
#                    'medium_url': 'https://static.inaturalist.org/photos/7885442/medium.jpg?1495165836',
#                    'original_dimensions': {'height': 800, 'width': 1200},
#                    'square_url': 'https://static.inaturalist.org/photos/7885442/square.jpg?1495165836',
#                    'url': 'https://static.inaturalist.org/photos/7885442/square.jpg?1495165836'},
#  'extinct': False,
#  'flag_counts': {'resolved': 1, 'unresolved': 1},
#  'iconic_taxon_id': 3,
#  'iconic_taxon_name': 'Aves',
#  'id': 12716,
#  'is_active': True,
#  'matched_term': 'Turdus merula',
#  'name': 'Turdus merula',
#  'observations_count': 21840,
#  'parent_id': 12705,
#  'preferred_common_name': 'Eurasian Blackbird',
#  'rank': 'species',
#  'rank_level': 10,
#  'taxon_changes_count': 1,
#  'taxon_schemes_count': 6,
#  'wikipedia_url': 'http://en.wikipedia.org/wiki/Common_blackbird'}

"http://api.inaturalist.org/v1/observations?identified=true&photos=true&identifications=most_agree&quality_grade=research&order=desc&order_by=created_at&taxon_id=41944&place_id=1&per_page=200"


def get_inat_photos():
    birdsfile = 'berlin-birds-extended-inat.csv'
    with open(birdsfile, newline='',encoding='utf8') as csvfile:
            birdreader = csv.DictReader(csvfile, delimiter=';')
            for row in birdreader:
                logging.info("Getting observations for {0}. Taxa ID {1}".format(row["name"], row["inat_id"]))
                print("Getting observations for {0}. Taxa ID {1}".format(row["name"], row["inat_id"]))
                collect_inat_photos(row)
                
 
def collect_inat_photos(row):
    params = {"identified":"true",
                "photos":"true",
                "identifications":"most_agree",
                "quality_grade":"research",
                "order":"desc",
                "order_by":"created_at",
                "per_page":200}
    params["taxon_id"] = row["inat_id"]
    params["place_id"] = 7207

    obs = get_all_observations(params=params)
    logging.info("Received {0} observations for {1} ".format(len(obs),row["name"]))
    print("Received {0} observations for {1} ".format(len(obs),row["name"]))

    phs = []
    for result in obs:
        logging.debug("Found {0} photos for {1} ".format(len(result["photos"]),row["name"]))
        #print("Found {0} photos for {1} ".format(len(result["photos"]),row["name"]))
        for photo in result["photos"]:
            phs.append(photo["url"].replace("square","medium"))

    with shelve.open('inat_photos') as db:
        print("Writing {0} photos for {1} ".format(len(phs),row["name"]))
        logging.info("Writing {0} photos for {1} ".format(len(phs),row["name"]))
        db[row["name"]] = phs



def get_db_birds():
    # d = shelve.open("inat_photos_fixed")
    with shelve.open('inat_photos_fixed') as db:
        for bird in db:
            print(bird)
        # birdsfile = 'berlin-birds-extended-inat.csv'
        # with open(birdsfile, newline='',encoding='utf8') as csvfile:
        #     birdreader = csv.DictReader(csvfile, delimiter=';')
        #     for row in birdreader:
        #         try:
        #             #print(db[row["name"]])
        #             name = row["name"]
        #             d[name] = db[name]
        #         except Exception as e:
        #             print(e)
    # d.close()
                

#get_db_birds()

def fetch_url(entry,header,proxy):
    path, uri = entry
    #print("Download file {0} to {1}".format(uri, path))
    if not os.path.exists(path):
        print("Download file {0} to {1}".format(uri, path))
        try:
            r = requests.get(uri, stream=True,headers=header,proxies=proxy,timeout=5)
        except Exception as e:
            r = requests.get(uri, stream=True,headers=header)
        finally:
            return None
        if r.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        else:
            print("Problem with download {0}".format(r.status_code))
    return path


def create_downloads(bird_name, bird_urls):
    i = 0
    entries = []
    bird_path = os.path.join("data",bird_name)
    if not os.path.exists(bird_path):
        os.mkdir(bird_path)

    for url in bird_urls:
        if i<= 300:
            dest = os.path.join("data",bird_name,"{0}_{1}.jpg".format(str(bird_name).lower(),i))
            entries.append((dest,url))
            i+=1
        else:
            print("Got {0} entries. Exiting".format(len(entries)))
            break
    return entries


def download_image(entries):
    #print("Downloading {0}".format(entries))
    #results = ThreadPool(4).imap_unordered(fetch_url, entries)

    proxies = prepare_proxies()
    ua = UserAgent()    

    for entry in entries:
        header = {'User-Agent':str(ua.chrome)}
        proxy = random.choice(proxies)
        print("Using proxy: {0}".format(proxy))  
        fetch_url(entry, header, proxy)
    #for path in results:
    #    print(path)

def download_images():
    with shelve.open('inat_photos') as db:
        birdsfile = 'berlin-birds-extended-inat.csv'
        with open(birdsfile, newline='',encoding='utf8') as csvfile:
            birdreader = csv.DictReader(csvfile, delimiter=';')
            for row in birdreader:
                try:
                    images = db[row["name"]]
                except Exception as e:
                    print("No images available")
                print("We have {0} URLs for {1}".format(len(images), row["name"]))
                if len(images) > 0:
                    urls = create_downloads(row["name"],images)
                    print("We got {0} for {1}".format(len(urls), row["name"]))
                    download_image(urls)


#get_inat_photos()
download_images()

