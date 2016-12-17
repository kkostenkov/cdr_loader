
class ClientData:
   
    def __init__(self, client_name, ip, login, passw, db_name, table_name, api_key, crm_url):
        self.name = client_name
        self.ip = ip
        self.login = login
        self.password = passw
        self.db_name = db_name
        self.table_name = table_name
        self.api_key = api_key
        self.retailcrm_url = crm_url
        
    def __str__(self):
        return "\n".join((self.name,
                          self.ip, 
                          self.login, 
                          self.password, 
                          self.name, 
                          self.table_name, 
                          self.api_key, 
                          ))