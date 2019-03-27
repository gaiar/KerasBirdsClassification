import glob, os,shutil
import filetype

DATA_DIR = "data"

def rename_downloads():
    for dirname in os.listdir(DATA_DIR):
        dirname = os.path.join(os.getcwd(),DATA_DIR,dirname)
        if os.path.isdir(dirname):
            for i, filename in enumerate(os.listdir(dirname)):
                if not os.path.isdir(os.path.join(dirname,filename)):
                    _, ext = os.path.splitext(os.path.basename(filename))
                    ext = ext.lower()
                    kind = filetype.guess(os.path.join(dirname,filename))
                    if kind is not None:
                        ext = ".{0}".format(kind.extension)
                    else:
                        try:
                            print("[WARN] :: Deleting {0}".format(filename))
                            os.remove(os.path.join(dirname,filename))
                            continue
                        except Exception:
                            print("[ERROR] :: Problem deleting {0}".format(filename))
                    new_name = "{0}_{1}{2}".format(
                        os.path.basename(dirname).lower(),
                        str(i),
                        ext
                        )
                    print("[INFO] :: Renaming {0} to {1}".format(filename,new_name))           
                    try:
                        os.rename(os.path.join(dirname,filename),os.path.join(dirname,new_name))
                    except Exception:
                        print("[ERROR] :: Failed renaming {}".format(
                            os.path.join(dirname,filename)
                        ))
                else:
                    print("[INFO] :: {0} is directory. Skipping.".format(filename))

rename_downloads()