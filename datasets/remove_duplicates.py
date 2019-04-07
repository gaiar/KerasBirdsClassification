#!/usr/bin/env python
import sys
import os
import hashlib
import logging
logging.basicConfig(
    filename='duplicates.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

SOURCE_DIR = "duplicates"
DULICATES_DEST = "dupdup"


def move_file(source_file, dest_file):
    try:
        os.rename(source_file, dest_file)
    except Exception as e:
        print("[ERROR] :: Failed renaming {}".format(
            source_file
        ))
        logging.error("Failed renaming {0}. Problem is {1}".format(
            source_file, e
        ))


def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk


def get_hash(filename, first_chunk_only=False, hash=hashlib.sha1):
    hashobj = hash()
    file_object = open(filename, 'rb')

    if first_chunk_only:
        hashobj.update(file_object.read(1024))
    else:
        for chunk in chunk_reader(file_object):
            hashobj.update(chunk)
    hashed = hashobj.digest()

    file_object.close()
    return hashed


def check_for_duplicates(source_dir, dest_dir, hash=hashlib.sha1):
    hashes_by_size = {}
    hashes_on_1k = {}
    hashes_full = {}

    for dirpath, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            try:
                # if the target is a symlink (soft one), this will
                # dereference it - change the value to the actual target file
                full_path = os.path.realpath(full_path)
                file_size = os.path.getsize(full_path)
            except (OSError,):
                # not accessible (permissions, etc) - pass on
                logging.error("File {0} not accessible".format(full_path))
                continue

            duplicate = hashes_by_size.get(file_size)

            if duplicate:
                hashes_by_size[file_size].append(full_path)
            else:
                # create the list for this file size
                hashes_by_size[file_size] = []
                hashes_by_size[file_size].append(full_path)

    # For all files with the same file size, get their hash on the 1st 1024 bytes
    for __, files in hashes_by_size.items():
        if len(files) < 2:
            continue    # this file size is unique, no need to spend cpy cycles on it

        for filename in files:
            try:
                small_hash = get_hash(filename, first_chunk_only=True)
            except (OSError,):
                # the file access might've changed till the exec point got here
                continue

            duplicate = hashes_on_1k.get(small_hash)
            if duplicate:
                hashes_on_1k[small_hash].append(filename)
            else:
                # create the list for this 1k hash
                hashes_on_1k[small_hash] = []
                hashes_on_1k[small_hash].append(filename)

    # For all files with the hash on the 1st 1024 bytes, get their hash on the full file - collisions will be duplicates
    for __, files in hashes_on_1k.items():
        if len(files) < 2:
            continue    # this hash of fist 1k file bytes is unique, no need to spend cpy cycles on it

        for filename in files:
            try:
                full_hash = get_hash(filename, first_chunk_only=False)
            except (OSError,):
                # the file access might've changed till the exec point got here
                continue

            duplicate = hashes_full.get(full_hash)
            if duplicate:
                print("Duplicate found: {0} and {1}".format(
                    filename, duplicate))
                logging.info("Duplicate found: {0} and {1}".format(
                    filename, duplicate))
                dest_file = os.path.join(os.getcwd(), DULICATES_DEST, os.path.basename(os.path.dirname(filename)),os.path.basename(filename))
                print("Moving duplicate {0} to {1}".format(filename,dest_file))
                logging.info("Moving duplicate {0} to {1}".format(filename,dest_file))
                move_file(filename,dest_file)
            else:
                hashes_full[full_hash] = filename


def get_directory(base_dir, bird_name):
    directory = os.path.join(os.getcwd(), base_dir, bird_name)
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


def clean_duplicates():
    for dirname in os.listdir(SOURCE_DIR):
        source_dir = os.path.join(os.getcwd(), SOURCE_DIR, dirname)
        dest_dir = get_directory(DULICATES_DEST, dirname)
        logging.debug("Checking duplicates in {0}".format(source_dir))

        if os.path.isdir(source_dir):
            check_for_duplicates(source_dir, dest_dir)

clean_duplicates()