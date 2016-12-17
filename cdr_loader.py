#!usr/bin/python
# -*- coding: utf-8 -*-

from database.database import fetch_calls
from database.clients import get_database_for_client
from crm.crm import upload_calls
from settings import defaultDb

def print_fetched(fetched_data):
    from pprint import pprint
    pprint(fetched_data)

#get_database_for_client("first client")
calls = fetch_calls(defaultDb)
#print_fetched(calls)
upload_calls(calls)


