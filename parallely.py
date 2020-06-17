import time, threading, subprocess, sys
from queue import Queue

lock = threading.Lock()
q = Queue()

filename = sys.argv[1]
url_list = []
with open(filename,'r') as file:
    url_list = file.read().split("\n")

for worker in url_list:
    q.put(worker)

start = time.time()

def download(worker):
    check = subprocess.run(["wget",worker],stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if check != 0 :
        with lock:
            print("Downloaded file from url: ",worker)

def threader():
    while True:
        worker = q.get()
        download(worker)
        q.task_done()

for x in range(10):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

q.join()
print("Total time taken to download files: ", time.time()-start)