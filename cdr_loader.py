#!usr/bin/python
# -*- coding: utf-8 -*-


from crm.crm import upload_calls
from database.database import fetch_calls
from database.clients import get_infos_of_clients
import settings
from utils import get_client_names, backup_log_file, setup_logging
import logging
import threading

def print_fetched(fetched_data):
    from pprint import pprint
    pprint(fetched_data)

def manual_upload():
    logging.info("Manual upload. Using data from settings.py")
    info = settings.defaultDb
    calls = fetch_calls(info)
    upload_calls(calls, info.api_key, info.retailcrm_url)
    
def Main():
    if settings.options.manual_upload: # Upload only one custom client.
        manual_upload()
        return
        
    clients = get_client_names()
    client_infos = get_infos_of_clients(clients)
    for info in client_infos: 
        logging.info("____________Client %s__________", info.name)
        calls = fetch_calls(info)
        upload_calls(calls, info.api_key, info.retailcrm_url)

setup_logging()
logging.info("Script started.")
worker = threading.Thread(target=Main, name="Main thread")
worker.daemon = True
worker.start()
limit = settings.options.execution_timelimit
if limit > 0:
    logging.info("Running with timelimit %s" % limit)
    worker.join(float(limit))
else:
    logging.info("Running without timelimit")
    worker.join()
if worker.isAlive():
    logging.error("Script runtime exceeded allowed time and was interrupted")
    backup_log_file()
logging.info("Script ended.")