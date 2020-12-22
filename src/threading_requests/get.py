import requests
import threading, queue

import authorization

#lock = threading.Semaphore(20)

def parse(url, response_q):
    r = requests.get(url, headers=authorization.get_token_headers())
    #lock.release()
    response_q.put(r)

def get(urls):
    thread_pool = []
    responses = []
    response_q = queue.Queue()
    for url in urls:
        thread = threading.Thread(target=parse, args=(url, response_q,))
        thread_pool.append(thread)
        thread.start()
        print("1 more thread")
        responses.append(response_q.get())
        #lock.acquire()
    for thread in thread_pool:
        thread.join()
    return responses
