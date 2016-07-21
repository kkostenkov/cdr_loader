#!usr/bin/python
# -*- coding: utf-8 -*-

from commands import getoutput as bash
from optparse import OptionParser

db_ip = "localhost"
db_login = "cdr_fetcher"  # permissions SELECT, UPDATE
#find_user = "cat /etc/asterisk/cdr_mysql.conf|grep user$"
#db_login = bash(find_user)[7:]
#find_passw = 'cat /etc/asterisk/cdr_mysql.conf|grep password'
db_pass = "cdr911"
#db_pass = bash(find_passw)
db_name  = "asteriskcdrdb"
#db_name  = "cdr"
table_name = "cdr"

api_path =  "/api/v3/telephony/calls/upload"
crm_url = "https://agmashop.retailcrm.ru"
api_url = "".join((crm_url, api_path))

client_id = "bffc6f6bbdc14bee86df"  # 20 numbers and digits    
records_url = "https://sip.agemas.it-d.it/ITD/getrecord.php"

max_call_entries = 50 # per POST message
upload_delay_minutes = 2 # don't upload entries younger than this value

api_key = "Enter your secret key here"

parser = OptionParser()
parser.add_option("--minutes",
                   default=0,
                  help="Maximum age of entries to fetch from database in minutes. Concatenates with --hours, --days, --weeks")                  
parser.add_option("--hours",
                   default=0,
                  help="Maximum age of entries to fetch from database in hours. Concatenates with --minutes, --days, --weeks")                     
parser.add_option("--days",
                   default=0,
                  help="Maximum age of entries to fetch from database in days. Concatenates with --minutes, --hours, --weeks") 
parser.add_option("--weeks",
                   default=0,
                  help="Maximum age of entries to fetch from database in weeks. Concatenates with --minutes, --hours, --days") 
parser.add_option("--minimum_duration",
                   default=0,
                  help="Minimum duration of calls to fetch (in minutes)")                           
options, args = parser.parse_args()  
