import MySQLdb
from settings import all_clietns_db, default_cdrdb_table_name
from data import DatabaseInfo

only_active = True

def _get_db_connection(dbInfo):    
    """ Returns connection or states error"""
    db = MySQLdb.connect(host=dbInfo.ip, user=dbInfo.login, passwd=dbInfo.password, db=dbInfo.name, charset="utf8")
    return db
    
def get_database_for_client(clientName):
    # Create connection
    connection  = _get_db_connection(all_clietns_db)
    if connection is None: 
        print "DB connection is none"
        return None
    cursor = connection.cursor()
    
    # compose MySQL query
    columns = ("mysql_host", "mysql_user", "mysql_pass", "mysql_db")
    columns_string = ", ".join(columns)
    query = "SELECT %s FROM %s.%s WHERE name = '%s'" % (columns_string, all_clietns_db.name, all_clietns_db.table_name, clientName)
    # Only active clients?
    if only_active:
        query += " AND active = 1"
    # execute query
    #print query
    cursor.execute(query)
    data = cursor.fetchall()
    # Validate fetched data
    if len(data) == 0:
        print "no entry for client with name %s found" % (clientName)
        connection.close()
        return
    
    # populate DatabaseInfo
    for host, user, passw, db_name in data:
        table_name = default_cdrdb_table_name
        client_db = DatabaseInfo(host, user, passw, db_name, table_name)
        #print client_db
    connection.close()
    return client_db
    
def get_known_clinet_names(only_active=False):
    # Create connection
    connection  = _get_db_connection(all_clietns_db)
    if connection is None: 
        print "DB connection is none"
        return None
    cursor = connection.cursor()
    
    # compose MySQL query
    query = "SELECT name FROM %s.%s" % (all_clietns_db.name, all_clietns_db.table_name)
    if only_active:
        query += " WHERE active = 1"
    #print query
    # execute query
    cursor.execute(query)
    data = cursor.fetchall()
    
    # Validate fetched data
    if len(data) == 0:
        print "No active clients in database"
        connection.close()
        return
        
    known_names = [name[0] for name in data]
    print known_names
    connection.close()
    return known_names
    
def get_databases_for_clients(clients):
    databases = []
    for client in clients:
        client_db_info = get_database_for_client(client)
        if client_db_info:
            databases.append(client_db_info)
    return databases
            