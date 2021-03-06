#!usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from data import ClientData

# ____________ Custom client data __________________
name = "default client data"
db_ip = "localhost"
db_login = "cdr_fetcher"  # permissions SELECT, UPDATE
db_pass = "cdr911"
db_name  = "asteriskcdrdb"
default_cdrdb_table_name = "cdr"
api_key = "Enter your secret key here"
crm_url = "https://agmashop.retailcrm.ru"
defaultDb = ClientData(name, db_ip, db_login, db_pass, db_name, default_cdrdb_table_name, api_key, crm_url)

# ____________ Client info database data__________________
name = "All client's database info"
db_ip = "localhost"
db_login = "rcrm"  
db_pass = "123$qaz"
db_name  = "rcrm"
table_name = "clients"
all_clients_db = ClientData(name, db_ip, db_login, db_pass, db_name, table_name, api_key=None, crm_url=None)

# ____________ Retail CRM API  ______________________
api_path =  "/api/v4/telephony/calls/upload"
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
parser.add_option("--manual_upload",
                   action="store_true",
                   dest="manual_upload",
                   default = False,
                   help="Use Default client data from settings file instead of database.")                      
parser.add_option("--execution_timelimit",
                   default=0,
                  help="Maximum limit for script execution time (in seconds)")      
parser.add_option("--logfile",
                   default="general.log",
                  help="Custom name of logfile")   
parser.add_option("-d",
                   action="store_true",
                   dest="debug_mode",
                   default = False,
                   help="Run in debug logging mode.")                          
                   
options, args = parser.parse_args()  
