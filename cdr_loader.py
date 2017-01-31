#!usr/bin/python
# -*- coding: utf-8 -*-


from crm.crm import upload_calls
from database.database import fetch_calls
from database.clients import get_infos_of_clients
import settings
from utils import get_client_names, use_debug_logging
import logging

def print_fetched(fetched_data):
    from pprint import pprint
    pprint(fetched_data)

def Main():   
    if settings.options.manual_upload: # Upload only one custom client.
        logging.info("Manual upload. Using data from settings.py")
        info = settings.defaultDb
        calls = fetch_calls(info)
        upload_calls(calls, info.api_key, info.retailcrm_url)
        return
        
    clients = get_client_names()
    client_infos = get_infos_of_clients(clients)
    for info in client_infos: 
        logging.info("____________Client %s__________", info.name)
        calls = fetch_calls(info)
        upload_calls(calls, info.api_key, info.retailcrm_url)


use_debug_logging()
logging.basicConfig(filename="general.log", 
                    #filemode='w',    # if uncommented - rewrites file each time
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s', 
                    datefmt='%d/%m/%Y %H:%M:%S',
                    )
logging.info("Script started.")
Main()
logging.info("Script ended.")