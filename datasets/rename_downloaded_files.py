import glob, os,shutil

def rename(dir, pattern, titlePattern):
    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        os.rename(pathAndFilename, 
                  os.path.join(dir, titlePattern % title + ext))

def rename_downloads():
    for dirname in os.listdir("downloads"):
        dirname = os.path.join(os.getcwd(),"downloads",dirname)
        if os.path.isdir(dirname):
            for i, filename in enumerate(os.listdir(dirname)):
                _, ext = os.path.splitext(os.path.basename(filename))
                ext = ext.lower()
                if ext not in (".jpg",".jpeg",".gif",".png",".bmp",".tiff"):
                    ext = ".jpg"
                new_name = "{0}_{1}{2}".format(
                    os.path.basename(dirname).lower(),
                    str(i),
                    ext
                    )
                print("Renaming {0} to {1}".format(filename,new_name))           
                try:
                    os.rename(os.path.join(dirname,filename),os.path.join(dirname,new_name))
                except Exception:
                    print("Failed renaming {}".format(
                        os.path.join(dirname,filename)
                    ))


rename_downloads()