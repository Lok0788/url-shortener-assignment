# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL mappings
# - Tracking click counts
# - Managing URL metadata
from datetime import datetime
from threading import Lock

#in memory dictionary to store URL mapping and metadate
url_db={}
lock =Lock()
def store_url_mapping(short_code,original_url):
    with lock:
        url_db[short_code]={
            'url':original_url,
            'Clicks':0,
            'created_at':datetime.utcnow().isoformat()
        }
def get_original_url(short_code):
    with lock:
        return url_db.get(short_code)

def increment_clicks(short_code):
    with lock:
        if short_code in url_db:
            url_db[short_code]['Clicks']+=1      

def get_stats(short_code):
    with lock:
        return url_db.get(short_code)