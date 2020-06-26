# -*- coding: utf-8 -*-
#!/usr/bin/python

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from threading import Thread
import time
import re
import os

class Watcher:
    print('Start Wathdogs')
    DIRECTORY_TO_WATCH = "C:/"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True: time.sleep(5)
        except:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod    
    def on_any_event(event):
        p = re.compile(r"[$]Recycle")
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            print ("[+] %s." % event.src_path)
            fname, ext = os.path.splitext(event.src_path)
            if (ext == '.exe'):
                time.sleep(1)
                del categorylist[0:]
                print ("[x] - %s." % event.src_path)
                w_filename = fname+ext

                if(re.search(p, event.src_path)): pass
            else: pass
            
if __name__ == '__main__':
    w = Watcher()
    
    WatchdogThread = Thread(target=w.run)
    WatchdogThread.start()

    
