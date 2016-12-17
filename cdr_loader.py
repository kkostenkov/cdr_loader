#!usr/bin/python
# -*- coding: utf-8 -*-

from database.database import fetch_calls
from database.clients import get_databases_for_clients
from crm.crm import upload_calls
#from settings import defaultDb
from utils import get_client_names

def print_fetched(fetched_data):
    from pprint import pprint
    pprint(fetched_data)
    
clients = get_client_names()
databases = get_databases_for_clients(clients)
for db in databases: 
    calls = fetch_calls(db)
    #print_fetched(calls)
    upload_calls(calls)




