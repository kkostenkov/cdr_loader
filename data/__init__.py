
class ClientData:
   
    def __init__(self, ip, login, passw, db_name, table_name, api_key=None, crm_url=None):
        self.ip = ip
        self.login = login
        self.password = passw
        self.name = db_name
        self.table_name = table_name
        self.api_key = api_key
        self.retailcrm_url = crm_url
        
    def __str__(self):
        return "\n".join((self.ip, 
                          self.login, 
                          self.password, 
                          self.name, 
                          self.table_name, 
                          self.api_key, 
                          ))