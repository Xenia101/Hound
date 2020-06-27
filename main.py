# -*- coding: utf-8 -*-
#!/usr/bin/python

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from threading import Thread
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont
import tkinter.ttk as ttk
import requests
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

    def upload(self, file_, api_key):
        params = {"api_key": API,"filename": file_}
        files = {"file": (file_, open(file_, "rb"), 'application/octet-stream')}
        response = requests.post("https://public.api.malwares.com/v3/file/upload", files=files, data=params)
        json_response = response.json()
        hash = json_response['sha256']
        print(hash)
        return hash

class Handler(FileSystemEventHandler):
    @staticmethod    
    def on_any_event(event):
        p = re.compile(r"[$]Recycle")
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            fname, ext = os.path.splitext(event.src_path)
            if (ext == '.exe'):
                w_filename = fname+ext
                print(w_filename)
                if(re.search(p, event.src_path)): pass
            else: pass

class MultiColumnListbox(object):
    def __init__(self):
        self.tree = None
        self._setup_widgets()
        self._build_tree()

    def _setup_widgets(self):
        container = ttk.Frame()
        container.pack(fill='both', expand=True)
        self.tree = ttk.Treeview(columns=category, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

    def _build_tree(self):
        for col in category:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        for item in categorylist:
            self.tree.insert('', 'end', values=item)
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(category[ix],width=None)<col_w:
                    self.tree.column(category[ix], width=col_w)

# window setting
window = Tk()
window.title("미션 2")

frame1 = Frame(window, height=200, width=300)

frame1.pack()

AnalysisButton = Button(frame1, height=2, width=32, text = "분석요청", command = openfile)
AnalysisButton.grid(row=1, column=0, padx=(5, 5), pady=(5, 5))

ResultSave = Button(frame1, height=2, width=32, text = "결과저장", command = filesave)
ResultSave.grid(row=1, column=2, padx=(5, 5), pady=(5, 5))

category = ['파일명(원본)', '파일명(SHA256)', '파일조회결과']

categorylist = []            
          
if __name__ == '__main__':
    listbox = MultiColumnListbox()
    w = Watcher()
    
    WatchdogThread = Thread(target=w.run)
    WatchdogThread.start()

    
