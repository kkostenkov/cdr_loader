import MySQLdb
import logging
from settings import all_clients_db, default_cdrdb_table_name
from data import ClientData

def _get_db_connection(dbInfo):    
    """ Returns connection or states error"""
    db = MySQLdb.connect(host=dbInfo.ip, user=dbInfo.login, passwd=dbInfo.password, db=dbInfo.db_name, charset="utf8")
    return db
    
def get_info_for_client(clientName):
    # Create connection
    logging.debug("Getting info for client %s", clientName)
    connection  = _get_db_connection(all_clients_db)
    if connection is None: 
        logging.warning("DB connection is none")
        return None
    cursor = connection.cursor()
    
    # compose MySQL query
    columns = ("mysql_host", "mysql_user", "mysql_pass", "mysql_db", "apikey", "retailcrm_url")
    columns_string = ", ".join(columns)
    query = "SELECT %s FROM %s.%s WHERE name = '%s'" % (columns_string, all_clients_db.db_name, all_clients_db.table_name, clientName)
    # execute query
    logging.debug(query)
    cursor.execute(query)
    data = cursor.fetchall()
    # Validate fetched data
    if len(data) == 0:
        #print "no entry for client with name %s found" % (clientName)
        logging.warning("no entry for client with name %s found", clientName)
        connection.close()
        return
    
    # populate ClientData
    for host, user, passw, db_name, api_key, crm_url in data:
        table_name = default_cdrdb_table_name
        client_db = ClientData(clientName, host, user, passw, db_name, table_name, api_key, crm_url)
        #print client_db
        logging.debug(client_db)
    connection.close()
    return client_db
    
def get_known_clinet_names(only_nonblocked=True):
    # Create connection
    connection  = _get_db_connection(all_clients_db)
    if connection is None: 
        print "DB connection is none"
        logging.warning("DB connection is none")
        return None
    cursor = connection.cursor()
    
    # compose MySQL query
    query = "SELECT name FROM %s.%s" % (all_clients_db.db_name, all_clients_db.table_name)
    if only_nonblocked:
        logging.info("only nonblocked")
        query += " WHERE blocked = 0"
    logging.debug(query)
    # execute query
    cursor.execute(query)
    data = cursor.fetchall()
    
    # Validate fetched data
    if len(data) == 0:
        logging.info("No active clients in database")
        connection.close()
        return
        
    known_names = [name[0] for name in data]
    logging.debug(known_names)
    connection.close()
    return known_names
    
def get_infos_of_clients(clients):
    databases = []
    for client in clients:
        client_db_info = get_info_for_client(client)
        if client_db_info:
            databases.append(client_db_info)
    logging.info("Got info for %s clients", len(databases))
    return databases
            