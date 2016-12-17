#!usr/bin/python
# -*- coding: utf-8 -*-

from database.database import fetch_calls
from database.clients import get_infos_of_clients
from crm.crm import upload_calls
#from settings import defaultDb
from utils import get_client_names

def print_fetched(fetched_data):
    from pprint import pprint
    pprint(fetched_data)
    
clients = get_client_names()
print "Clients to process: %s" % (clients)
client_infos = get_infos_of_clients(clients)
for info in client_infos: 
    print "____________Client %s__________" % (info.name)
    calls = fetch_calls(info)
    #print_fetched(calls)
    upload_calls(calls, info.api_key, info.retailcrm_url)




