import glob
import os
import shutil
import filetype
import logging

logging.basicConfig(
    filename='renaming.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

DATA_SOURCE_DIR = "duplicates"
DATA_DEST_DIR = "data"


def delete_file(filename):
    try:
        print("[WARN] :: Deleting {0}".format(filename))
        logging.warning("Deleting {0}".format(filename))
        os.remove(filename)
    except Exception:
        print(
            "[ERROR] :: Problem deleting {0}".format(filename))
        logging.error(
            "Problem deleting {0}".format(filename))


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


#DATA_DIR = "data-clean"


def rename_downloads():
    for dirname in os.listdir(DATA_SOURCE_DIR):
        source_dir = os.path.join(os.getcwd(), DATA_SOURCE_DIR, dirname)
        dest_dir = get_directory(DATA_DEST_DIR,dirname)

        logging.debug("Copying files from {0} to {1}".format(source_dir,dest_dir))

        if os.path.isdir(source_dir):
            for i, filename in enumerate(os.listdir(source_dir)):
                if not os.path.isdir(os.path.join(source_dir, filename)):
                    ext = ""
                    kind = filetype.guess(os.path.join(source_dir, filename))

                    if kind is not None:
                        logging.debug("File {0} has type of {1}".format(
                            filename, kind.mime))
                        ext = ".{0}".format(kind.extension)
                    else:
                        delete_file(os.path.join(source_dir, filename))
                        continue

                    n = len(os.listdir(dest_dir))
                    logging.debug("{0} :: {1} of files".format(dest_dir,n))

                    new_name = "{0}_{1}{2}".format(
                        os.path.basename(dest_dir).lower().replace(" ", "_"),
                        str(n+1),
                        ext
                    )
                    print("[INFO] :: Renaming {0} to {1}".format(
                        filename, new_name))
                    logging.info("Renaming {0} to {1}".format(
                        filename, new_name))

                    source_file = os.path.join(source_dir, filename)
                    dest_file = os.path.join(dest_dir, new_name)
                    move_file(source_file, dest_file)
                else:
                    print(
                        "[INFO] :: {0} is directory. Skipping.".format(filename))
                    logging.info(
                        "{0} is directory. Skipping.".format(filename))


rename_downloads()
