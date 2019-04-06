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


DATA_DIR = "data-clean"


# import os, os.path

# # simple version for working with CWD
# print len([name for name in os.listdir('.') if os.path.isfile(name)])

# # path joining version for other paths
# DIR = '/tmp'
# print len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

def rename_downloads():
    for dirname in os.listdir(DATA_DIR):
        dirname = os.path.join(os.getcwd(), DATA_DIR, dirname)
        if os.path.isdir(dirname):
            for i, filename in enumerate(os.listdir(dirname)):
                if not os.path.isdir(os.path.join(dirname, filename)):
                    ext = ""    
                    kind = filetype.guess(os.path.join(dirname, filename))
                    if kind is not None:
                        logging.debug("File {0} has type of {1}".format(filename, kind.mime))
                        ext = ".{0}".format(kind.extension)
                    else:
                        try:
                            print("[WARN] :: Deleting {0}".format(filename))
                            logging.warning("Deleting {0}".format(filename))
                            os.remove(os.path.join(dirname, filename))
                        except Exception:
                            print(
                                "[ERROR] :: Problem deleting {0}".format(filename))
                            logging.error(
                                "Problem deleting {0}".format(filename))
                        continue
                    new_name = "{0}_{1}{2}".format(
                        os.path.basename(dirname).lower().replace(" ", "_"),
                        str(i),
                        ext
                    )
                    print("[INFO] :: Renaming {0} to {1}".format(
                        filename, new_name))
                    logging.info("Renaming {0} to {1}".format(
                        filename, new_name))
                    try:
                        os.rename(os.path.join(dirname, filename),
                                  os.path.join(dirname, new_name))
                    except Exception as e:
                        print("[ERROR] :: Failed renaming {}".format(
                            os.path.join(dirname, filename)
                        ))
                        logging.error("Failed renaming {0}. Problem is {1}".format(
                            os.path.join(dirname, filename), e
                        ))
                else:
                    print(
                        "[INFO] :: {0} is directory. Skipping.".format(filename))
                    logging.info(
                        "{0} is directory. Skipping.".format(filename))


rename_downloads()
