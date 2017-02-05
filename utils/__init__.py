import logging
import os
import shutil
from settings import options as o
from database.clients import get_known_clinet_names

from time import gmtime, strftime

""" 
Parses names from command line args. If none given - fetches all names from DB.
Excludes specified names.
"""
def get_client_names():
    logging.info("Getting client names")
    names_to_fetch = []
    if o.clients is None:
        # fetch all clients from db
        given_names = get_known_clinet_names(only_nonblocked=True)
    else:
        given_names = o.clients.split(",")
        logging.info("%s client names provided from console", len(given_names))
    names_to_fetch = given_names
    logging.debug("clients before exclusion: %s" , (names_to_fetch))
    if o.exclude is not None:
        exclude_names = o.exclude.split(",")
        logging.debug("except %s", (exclude_names))
        logging.info("%s clients to exclude provided from console", len(exclude_names))
        left_names = [name for name in given_names if name not in exclude_names]
        names_to_fetch = left_names
    logging.debug("fetching clients: %s" , (names_to_fetch))
    logging.info("fetching %s clients" , len(names_to_fetch))
    return names_to_fetch
    

def setup_logging():
    if o.debug_mode:
        use_debug_logging()
    else:
        use_general_log()
   
def use_debug_logging():
    logging.basicConfig(filename=o.logfile,
                    filemode='w', 
                    format='%(asctime)s %(levelname)s:%(message)s', 
                    datefmt='%d/%m/%Y %H:%M:%S',
                    level=logging.DEBUG
                    )
    logging.info("Logging mode: DEBUG")

def use_general_log():
    logging.basicConfig(filename=o.logfile, 
                    filemode='w',    # if uncommented - rewrites file each time
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s', 
                    datefmt='%d/%m/%Y %H:%M:%S',
                    )
    logging.info("Logging mode: INFO")
                    
def backup_log_file():
    logging.info("Backing up logfile")
    logs_folder = "logs"
    filename =  strftime("%Y-%m-%d-%H_%M_%S", gmtime())+".log"
    endfile = os.getcwd() + os.sep + logs_folder + os.sep + filename
    shutil.copyfile(o.logfile, endfile)
    