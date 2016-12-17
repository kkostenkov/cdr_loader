#!usr/bin/python
# -*- coding: utf-8 -*-

from database.database import fetch_calls
from database.clients import get_known_clinet_names, get_databases_for_clients
from crm.crm import upload_calls
from settings import defaultDb

def print_fetched(fetched_data):
    from pprint import pprint
    pprint(fetched_data)



clients = get_known_clinet_names(only_active=True)
databases = get_databases_for_clients(clients)
for db in databases: 
    calls = fetch_calls(db)
    #print_fetched(calls)
    upload_calls(calls)




