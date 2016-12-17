This project fetches data from Asterisk database about phonecalls and uploads it to shop in Retailcrm.com


__________ <b>Entry point is cdr_loader.py</b> __________

Running it without arguments will upload all data from database.

Available arguments are maximum age of entries to fetch from database. Concatenates with each other.

* --minutes 

* --hours

* --days

* --weeks

For example:

*$ python cdr_loader.py --minutes=5 --hours=1*

will load all call data from 2 minutes old (setting in settings.py due to our server-side needs) to 65 minutes old.

Provide minimum duration of fetched calls (in minutes) via

* --minimum_duration

ex:

*$ python cdr_loader.py --minimum_duration=3*


* --clients

uses given names as list to fetch from database. If not specified - fetches all known active clients.
!No spaces in names allowed!

* --exclude
excludes given names from list of clients to fetch.
!No spaces in names allowed!

ex:
*$ python cdr_loader.py --clients=one_client,second_client*
will fetch two clients

*$ python cdr_loader.py --exclude=not_paying_client*
will fetch all active clients from database except "not_paying_client"

* --manual_upload 

Flag for Manual upload of single client. Prevents looking clients in database.
Gets Client info from settings.py file  "Custom client data" section. No argument needed.

ex:
*$ python cdr_loader.py --manual_upload *



cdr_loader.py uses two modules:

___________ <b>database</b> ___________

main func is fetch_calls()

calculates time interval for data to load

connects to db and loads needed data, changing db value format to Retailcrm format



___________ <b>crm</b> ___________

Provides connection to retailcrm shop and uploads data about calls to it.

upload_calls() takes dict of call data, divides them in groups of size, accepted by retailcrm and 

uses send_call_group() to load them one by one.

In case of response code 503 (too many requests from one client) tries two more times after some delay.


<b>!!!!  If all tries were unsuccessful just prints out response of server.  !!!!</b>

