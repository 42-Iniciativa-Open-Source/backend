import requests
import json
import threading
import queue
import time

import authorization

lock = threading.Semaphore(1)
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
        lock.acquire()
    for thread in thread_pool:
        thread.join()
    while not q.empty():
        responses.append(q.get())
    return responses


def data(urls: list, path: str) -> list:
    data = []
    headers = {}
    responses = get(urls)
    headers["X-Application-Name"] = []
    for r in responses:
        if r.status_code == requests.codes.ok:
            data.extend(json.loads(r.text))
            headers["X-Application-Name"].append(
                r.headers["X-Application-Name"]
            )
    return (data, headers)
