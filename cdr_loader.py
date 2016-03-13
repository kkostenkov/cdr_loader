#!usr/bin/python
# -*- coding: utf-8 -*-

from database.database import fetch_calls
from crm.crm import upload_calls

calls = fetch_calls()
upload_calls(calls)

    
