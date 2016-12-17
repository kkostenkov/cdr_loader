#!usr/bin/python
# -*- coding: utf-8 -*-

import json, time
import requests
from settings import api_path, max_call_entries

def upload_calls(calls, api_key, retailcrm_url):
    """ via using not standard lib """
    print "Uploading..."
    if calls is None:
        print "No calls to upload were given"
        return
    # divide by groups of acceptable length
    call_groups = list((calls[i:i+max_call_entries] for i in range(0,len(calls),max_call_entries)))
    # send each group
    for group in call_groups:
        response = send_call_group(group, api_key, retailcrm_url)
        if response is None:
            print "No response from api. Skipping."
            return
        code = response.status_code
        if code == 404: 
            print "Error!!! 404 NonFound %s \n Try to remove trailing slashes" % (retailcrm_url)
            return
        if code == 200: 
            print str(len(group)) + " calls sent successfully"
            continue
        tries = 1
        while code == 503 and tries < 3: # 2 more attempts to access busy API
            time.sleep(0.5) # wait for 0.5s
            reponse = send_call_group(group)
            code = response.status_code
            tries += 1
        response = json.loads(response.content.decode("utf-8"))
        if response["success"] == True: 
            print str(len(group)) + " calls sent successfully"
            continue
        # In case something went wrong:
        print(response)
        
def send_call_group(call_group, api_key, crm_url):
    calls_json = json.dumps(call_group)
    data = {"apiKey": api_key,
            "calls": calls_json,
            }
    api_url = "".join((crm_url, api_path))
    try:
        response = requests.post(api_url, data)
    except Exception:
        print "ERROR!!! Unhandeled exception: %s" % (Exception.message)
        print "Url was: %s" % (api_url)
        response = None
    return response
    
            
        
def get_request_example(api_key):
    import requests
    from  settings import crm_url
    url = "/api/v3/telephony/manager"
    api_url = "".join((crm_url, url))
    r = requests.get(api_url+("?phone=79213209879&apiKey=%s") % api_key)
    print(r)
     

if __name__ == "__main__":
    upload_calls("some call data")
    print("worked")