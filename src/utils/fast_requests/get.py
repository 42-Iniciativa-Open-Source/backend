import requests, threading, queue
import time

import authorization
from constants import APPS

lock = threading.Semaphore(2)
s = requests.Session()
q = queue.Queue()
q2 = queue.Queue()

def request(url: str):
    r = s.get(url, headers=authorization.get_token_headers())
    time.sleep(1)
    lock.release()
    q.put(r)

def get(urls: list) -> list:
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
    q2.put(responses)

def make_requests(urls: list) -> list:
    data = []
    amount_urls = len(urls)
    dividers = {800: 20, 600: 15, 400: 10, 200: 8, 100: 6, 50: 4, 10: 2}
    divider = dividers[amount_urls]
    
    parcel = round(len(urls) / divider)
    thread_pool = []
    responses = []
    print(parcel)
    for _ in range(divider):
        parcel_urls = urls[:parcel]
        thread = threading.Thread(target=get, args=(parcel_urls,))
        thread_pool.append(thread)
        thread.start()
        del urls[:parcel]
        print(f"1 more main thread.")
    for thread in thread_pool:
        thread.join()
    while not q2.empty():
        responses.extend(q2.get()) 

    #print(responses)
    #responses = get(urls)
    #errors = 0
    for r in responses:
        if r.status_code == requests.codes.ok:
            data.extend(r.json())
        #else:
        #    errors = errors + 1
    return data
