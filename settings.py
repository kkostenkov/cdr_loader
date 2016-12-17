#!usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from data import ClientData

# ____________ Default client data __________________
db_ip = "localhost"
db_login = "cdr_fetcher"  # permissions SELECT, UPDATE
db_pass = "cdr911"
db_name  = "asteriskcdrdb"
default_cdrdb_table_name = "cdr"
api_key = "Enter your secret key here"
crm_url = "https://agmashop.retailcrm.ru"
defaultDb = ClientData(db_ip, db_login, db_pass, db_name, default_cdrdb_table_name, api_key, crm_url)

# ____________ Client info database data__________________
db_ip = "localhost"
db_login = "rcrm"  
db_pass = "123$qaz"
db_name  = "rcrm"
table_name = "clients"
all_clients_db = ClientData(db_ip, db_login, db_pass, db_name, table_name)

# ____________ Retail CRM API  ______________________
api_path =  "/api/v3/telephony/calls/upload"



client_id = "bffc6f6bbdc14bee86df"  # 20 numbers and digits    
records_url = "https://sip.agemas.it-d.it/ITD/getrecord.php"

max_call_entries = 50 # per POST message
upload_delay_minutes = 2 # don't upload entries younger than this value



# ____________ Command line args parser __________________
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
parser.add_option("--clients",
                   default=None,
                  help="specify names of clients to upload")      
parser.add_option("--exclude",
                   default=None,
                  help="names of clients to ignore")      
options, args = parser.parse_args()  
