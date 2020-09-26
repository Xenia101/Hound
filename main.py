# -*- coding: utf-8 -*-
#!/usr/bin/python

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from threading import Thread
from tkinter import *
import tkinter.font as tkFont
import tkinter.ttk as ttk
import tkinter as tk
import requests
import os.path
import codecs
import json
import time
import re
import os

def openfile():
    del categorylist[0:]
    window.filename = filedialog.askopenfilenames(initialdir = "C:/",title = "파일을 선택하세요")
    file_count = len(window.filename)

    for x in range(file_count):
        num = summary(window.filename[x],API, upload(window.filename[x], API))
        if 0 <= num and num <= 10:
            file_list = [os.path.basename(window.filename[x]), upload(window.filename[x], API),    'normal'] # 일반 normal
        elif 10 < num and num <= 70:
            file_list = [os.path.basename(window.filename[x]), upload(window.filename[x], API), 'dangerous'] # 위험 dangerous
        elif 70 < num and num <= 100:
            file_list = [os.path.basename(window.filename[x]), upload(window.filename[x], API), 'malicious'] # 악성 malicious
        categorylist.append(file_list)
        
    listbox._build_tree()

def upload(file_, api_key):
    params = {"api_key": API,"filename": file_}
    files = {"file": (file_, open(file_, "rb"), 'application/octet-stream')}
    response = requests.post("https://public.api.malwares.com/v3/file/upload", files=files, data=params)
    json_response = response.json()
    hash = json_response['sha256']
    # print(hash)
    return hash

def summary(file_, api_key, hash_):
    params = {'api_key': API, 'hash': hash_}
    response = requests.get('https://public.api.malwares.com/v3/file/mwsinfo', params=params)
    json_response = response.json()
    json_result = json.dumps(json_response, indent=4, sort_keys=True)

    #if (json_response['behavior']['w7_32_kor']['security_level'] != None)
    #    security = json_response['behavior']['w7_32_kor']['security_level']

    ai_score = json_response['ai_score']
    # print(ai_score)
    return ai_score

def filesave():
    count = len(categorylist)
    f = codecs.open('output.csv', 'w', encoding='euc_kr')
    wr = csv.writer(f)
    wr.writerow(['번호', '파일명(원본)', '파일명(SHA256)', '파일조회결과'])
    for x in range(count):
        wr.writerow([x+1, categorylist[x][0], categorylist[x][1], categorylist[x][2]])
    f.close()

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
        #time.sleep(1)
        p = re.compile(r"[$]Recycle")
        if event.is_directory:
            return None
    
        elif event.event_type == 'created':
            print ("[+] %s." % event.src_path)
            
            # fname : path
            # ext   : filetype
            fname, ext = os.path.splitext(event.src_path)
            
            if (ext == '.exe'):
                time.sleep(1)
                del categorylist[0:]
                
                print ("[x] - %s." % event.src_path)
                w_filename = fname+ext

                if(re.search(p, event.src_path)):
                    print('[-]pass')
                    pass
                else:
                    #work to api                    
                    edit_filename = w_filename.replace('\\','/')

                    origin = edit_filename.split("/")
                    renameFile = origin[len(origin)-1]
                    print(renameFile) # original filename
    
                    params = {"api_key": API,"filename": edit_filename}
                    files = {"file": (edit_filename, open(edit_filename, "rb"), 'application/octet-stream')}
                    response = requests.post("https://public.api.malwares.com/v3/file/upload", files=files, data=params)
                    json_response = response.json()
                    print(json_response)
                    hash = json_response['sha256']
                    #print(hash) # print hash

                    params2 = {'api_key': API, 'hash': hash}
                    response2 = requests.get('https://public.api.malwares.com/v3/file/mwsinfo', params=params2)
                    json_response2 = response2.json()
                    security = json_response2['behavior']['w7_32_kor']['security_level']
                    print(json_response2)
                    ai_score = json_response2['ai_score']
                    #print(ai_score) # ai score

                    if 0 <= ai_score and ai_score <= 10:
                        file_list = [renameFile, hash,    'normal'] # 일반 normal
                    elif 10 < ai_score and ai_score <= 70:
                        file_list = [renameFile, hash, 'dangerous'] # 위험 dangerous
                    elif 70 < ai_score and ai_score <= 100:
                        file_list = [renameFile, hash, 'malicious'] # 악성 malicious

                    categorylist.append(file_list)
                    print('end')

                listbox._build_tree()
                
            else:
                print('[-] pass')
                pass

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
    window.mainloop()

    
