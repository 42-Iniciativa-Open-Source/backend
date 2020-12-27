import requests, json, threading, queue
import time

import authorization
from constants import APPS
from db.mongodb import mongo

mongo_conn = mongo.get_connection()

lock = threading.Semaphore(2)
s = requests.Session()
q = queue.Queue()
q2 = queue.Queue()

def request(url: str):
    r = s.get(url, headers=authorization.get_token_headers())
    time.sleep(0.5)
    lock.release()
    q.put(r)

def get(urls: list, fast: bool=False) -> list:
    thread_pool = []
    responses = []
    for url in urls:
        thread = threading.Thread(target=request, args=(url,))
        thread_pool.append(thread)
        thread.start()
        print(f"1 more thread {url}")
        lock.acquire()
    for thread in thread_pool:
        thread.join()
    while not q.empty():
        responses.append(q.get())
    if not fast:
        return responses
    else:
        q2.put(responses)

def fast_get(urls: list):
    divider = 20 
    parcel = round(len(urls) / divider)
    thread_pool = []
    responses = []
    for _ in range(divider):
        parcel_urls = urls[:parcel]
        thread = threading.Thread(target=get, args=(parcel_urls, True,))
        thread_pool.append(thread)
        thread.start()
        del urls[:parcel]
        print(f"1 more main thread.")
    for thread in thread_pool:
        thread.join()
    while not q2.empty():
        responses.extend(q2.get())
    return responses

def make_requests(urls: list, path: str) -> list:
    data = []
    db = mongo_conn["data"]
    cursor = db[path].find({}, {"_id": 0})
    for document in cursor:
        data.append(document)
    if not data:
        if len(urls) >= 20:
            responses = fast_get(urls)
        else:
            responses = get(urls)
        for r in responses:
            if r.status_code == requests.codes.ok:
                data.extend(json.loads(r.text))
        db[path].insert_many(data)
    return data
