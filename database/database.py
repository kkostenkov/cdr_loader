#!usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import MySQLdb
from settings import options as o
from settings import records_url, upload_delay_minutes


def _get_db_connection(dbInfo):    
    """ Returns connection or states error"""
    db = MySQLdb.connect(host=dbInfo.ip, user=dbInfo.login, passwd=dbInfo.password, db=dbInfo.name, charset="utf8")
    return db

def fetch_calls(dbInfo):        
    """ 
    Retrieves calls from database. If script options (--minutes, --hours,
    --days, --weeks) provided - uses them as maximum age of calls to fetch. 
    """
    m, h, d, w = int(o.minutes), int(o.hours), int(o.days), int(o.weeks)
    if m == 0 and h == 0 and d == 0 and w == 0:
        starttime = datetime.datetime.min
        print "Fetching all data from db"
    else:
        print "Fetching call data %d weeks, %d days, %d hours and %d minutes old maximum" % (w, d, h, m)                      
        starttime = datetime.datetime.now() - datetime.timedelta(minutes=m, hours=h, days=d, weeks=w)
        starttime = convert_datetime(starttime)
    # don't load too fresh entries
    endtime = datetime.datetime.now() - datetime.timedelta(minutes=upload_delay_minutes)
    # specify minimum duration
    min_duration = int(o.minimum_duration)
    if min_duration > 0:
        print "with minimum duration of fetched calls of %s minutes" % min_duration
    # connect
    try:
        connection  = _get_db_connection(dbInfo)
    except Exception:
        print "ERROR!! DB connection is none! Data was:"
        print dbInfo
        return None
    cursor = connection.cursor()
    # compose MySQL query
    columns = ("calldate", "dst", "src", "cnam", "disposition", "duration", "uniqueid", "recordingfile")
    columns_string = ", ".join(columns)
    query = "SELECT %s FROM %s.%s WHERE calldate > '%s' AND calldate < '%s'" % (columns_string, dbInfo.name, dbInfo.table_name, starttime, endtime)
    if min_duration > 0:
        query += "AND duration >= %s" % (min_duration)
    # execute query
    print query
    cursor.execute(query)
    data = cursor.fetchall()

    calls = []
    # populate calls list
    for calldate, dst, src, cnam, disposition, duration, uniqueid, recordingfile in data:
        call = {}    
        call["date"] = convert_datetime(calldate)    # Date and time of call (Y-m-d H:i:s)
        if len(dst) > 3:  # destination number more than 3 digits is  an outgoing call !TODO check for internal calls (150 -> 110)
            call["type"] = "out"
            call["phone"] = dst
            call["code"] = src
        else:
            call["type"] = "in"                          
            call["phone"] = src
            call["code"] = dst
        call["result"] = call_result(disposition)    # string call result
        call["duration"] = duration                  # integer	Lengh of conversation in seconds
        call["externalId"] = uniqueid                # string		uniq db ID 
        call["recordUrl"] = get_file_url_with_id(recordingfile) # URL to call record
        calls.append(call)    
    connection.close()
    print "Done."
    return calls
    
def convert_datetime(datetime):
    """ convert datetime class to sring of  (Y-m-d H:i:s) format """
    converted = datetime.strftime("%Y-%m-%d %H:%M:%S")
    return converted
    
def call_result(disp):
    """  possible results : failed, answered, busy, no answer, not allowed, unknown)"""
    # !TODO check if one can use .to_lower()
    result_map = { "ANSWERED": "answered",
                 "NO ANSWER": "no answer",
                 "BUSY": "busy",
                 "FAILED": "failed",
                 }
    disp = disp.decode("utf-8")
    if disp in result_map.keys():
        return result_map[disp]
    else: return "unknown"

def get_file_url_with_id(full_name):
    if full_name == "": return ""
    # get last part of string after "-" separator
    record_id = full_name.split("-")[-1]
    # cut the extention
    if record_id.endswith(".mp3") or record_id.endswith(".wav"):
        record_id = record_id[:-4]
    url =  "%s?record_id=%s" % (records_url, record_id)
    return url
