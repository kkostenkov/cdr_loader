#!usr/bin/python
# -*- coding: utf-8 -*-

from database.database import fetch_calls
from crm.crm import upload_calls
from settings import defaultDb

calls = fetch_calls(defaultDb)
upload_calls(calls)

    
