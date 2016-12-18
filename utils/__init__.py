from settings import options as o
from database.clients import get_known_clinet_names

""" 
Parses names from command line args. If none given - fetches all names from DB.
Excludes specified names.
"""
def get_client_names():
    names_to_fetch = []
    if o.clients is None:
        # fetch all clients from db
        given_names = get_known_clinet_names(only_nonblocked=True)
    else:
        given_names = o.clients.split(",")
    names_to_fetch = given_names
    #print "fetching clients: %s" & (names_to_fetch)
    if o.exclude is not None:
        exclude_names = o.exclude.split(",")
        #print "except %s" & (exclude_names)
        left_names = [name for name in given_names if name not in exclude_names]
        names_to_fetch = left_names
    return names_to_fetch