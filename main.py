import threading
from queue import Queue #threads cant just work directly with set or file
from spider import Spider
from domain import *
from general import *

PROJECT_NAME='wikipedia'
HOMEPAGE='https://www.wikipedia.org/'
DOMAIN_NAME=get_domain_name(HOMEPAGE)
QUEUE_FILE=PROJECT_NAME+'/queue.txt'
CRAWLED_FILE=PROJECT_NAME+'/crawled.txt'
NUMBER_OF_THREADS=4
queue=Queue() #thread queue

Spider(PROJECT_NAME,HOMEPAGE,DOMAIN_NAME)

#Multi-Threading
def create_threads():
    for x in range(NUMBER_OF_THREADS):
        t=threading.Thread(target=work) # work is the name of function
        t.daemon=True # Remember if removed thread will keep running if suddenly our program stops or if we stop it.
                      # This ensures that when main exits threads are killed
        t.start()

def work():
    while True:
        url=queue.get()
        Spider.crawl_page(threading.current_thread().name,url)
        queue.task_done() 

def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join() #to avoid dirty read problem
    crawl()

def crawl():
    queued_links=file_to_set(QUEUE_FILE)
    if len(queued_links > 0 ):
        print(str(len(queued_links))+' links in the queue')
        create_jobs

create_threads()
crawl()
