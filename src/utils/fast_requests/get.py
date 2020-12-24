import requests, threading, queue
import time

import authorization
from constants import APPS

lock = threading.Semaphore(int(APPS) * 2)
s = requests.Session()
q = queue.Queue()

def request(url: str):
    r = s.get(url, headers=authorization.get_token_headers())
    time.sleep(0.5)
    lock.release()
    q.put(r)

def get(urls: list) -> list:
    thread_pool = []
    responses = []
    for url in urls:
        thread = threading.Thread(target=request, args=(url,))
        thread_pool.append(thread)
        thread.start()
        responses.append(q.get())
        lock.acquire()
    for thread in thread_pool:
        thread.join()
    return responses

def make_requests(urls: list) -> list:
    data = []
    responses = get(urls)
    for r in responses:
        if r.status_code == requests.codes.ok:
            data.extend(r.json())
    return data
