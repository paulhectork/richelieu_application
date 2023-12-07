import os

from .constants import TMP 


# ********************************************
# filesystem operations: read and write to
# files and folders (io = input/output)
# ********************************************


def write_credfile(db:str) -> None:
    """
    create a file `TMP/credfile.txt` with the name of the
    `postgresql_credentials.json` file to use when creating 
    the engine. because `engine` must be available in the
    global context, it can't be called simply using a function,
    and we can't pass the filename as an argument from 
    `main` to `engine.py`.

    :param db: `local` or `server`, the `-d --database` 
               argument in the CLI
    """
    with open(os.path.join(TMP, "credfile.txt"), mode="w") as fh:
        fh.write("postgresql_credentials_local.json" if db=="local"
                 else "postgresql_credentials_remote.json")
    return


def read_credfile() -> str:
    """
    read the content of `TMP/credfile.txt` to return the name 
    of the credentials file to use when connecting to the db
    """
    with open(os.path.join(TMP, "credfile.txt"), mode="r") as fh:
        return fh.read()


def maketmp() -> None:
    """
    * delete the old TMP
    * create the new TMP and its child folders
    """
    os.makedirs(TMP)
    # os.makedirs(os.path.join(TMP, "imagefiles"))
    # os.makedirs(os.path.join(TMP, "imagefiles", "iconography"))
    # os.makedirs(os.path.join(TMP, "imagefiles", "cartography"))
    return


def deltmp(_dir:str=TMP) -> None:
    """
    delete all files/directories in the temp 
    directory + the dir itself, recursively.
    
    :param _dir: the directory to delete. this allows to use the function recursively
    """
    try:
        # check that the directory is in `TMP` to avoid deleting everything
        if not ( os.path.commonpath([ os.path.abspath(TMP) ]) 
                 == os.path.commonpath([ os.path.abspath(TMP), os.path.abspath(_dir) ]) 
        ):
            print(f"directory `{_dir}` not in TMP. not deleting the files and exiting")
            sys.exit(1)
        
        # delete recursively
        for root, dirs, files in os.walk(_dir):
            [ os.remove(os.path.join(root, f)) for f in files ]    
            [ deltmp(os.path.join(root, d)) for d in dirs ]
            
        # once you've deleted all its contents, delete itself `_dir`
        os.rmdir(_dir)  
        
    # pass if `_dir` is aldready deleted
    except FileNotFoundError:
        pass
    return


