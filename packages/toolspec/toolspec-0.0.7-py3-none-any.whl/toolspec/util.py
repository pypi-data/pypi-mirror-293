# -*- coding: utf-8 -*-
from urllib import request as Request
from queue import Queue
from functools import wraps
import multiprocessing
import threading
import configparser
import random, time, os
from tqdm import tqdm
import numpy as np


class LogHander:
    def __init__(self):
        self.__init_para(os.getcwd() + '\\ini.cfg', 'DEFAULT')
    def __init_para(self, file, section):
        cp = configparser.ConfigParser()
        cp.read(file, encoding='utf-8')
        self.__LOG_PATH = cp.get(section, 'LOG_PATH')
        self.__LOG_FILE = self.__LOG_PATH + '/' + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))  + '.log'
        if not os.path.exists(self.__LOG_PATH):
            os.mkdir(self.__LOG_PATH)
        self.__PLOCK = multiprocessing.Lock()
        self.__TLOCK = threading.Lock()
    def logging(self, text, error=False):
        if error:
            text = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' [ERROR]: '.ljust(10) + ('[' + multiprocessing.current_process().name + ']').ljust(15) + ('[' + threading.currentThread().name + ']').ljust(15) + text
        else:
            text = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' [INFO]: '.ljust(10) + ('[' + multiprocessing.current_process().name + ']').ljust(15) + ('[' + threading.currentThread().name + ']').ljust(15) + text
        self.__PLOCK.acquire()
        self.__TLOCK.acquire()
        print(text)
        open(self.__LOG_FILE, 'a', encoding='utf8').write(text + '\n')
        self.__TLOCK.release()
        self.__PLOCK.release()

class UrlHander:
    def __init__(self):
        self.__init_para(os.getcwd() + '\\ini.cfg', 'DEFAULT')
        self.__init_agent(os.getcwd() + '\\agent.lst')
    def __init_para(self, file, section):
        cp = configparser.ConfigParser()
        cp.read(file, encoding='utf-8')
        self.__TIME_OUT = int(cp.get(section, 'TIME_OUT'))
    def __init_agent(self, file):
        self.__USER_AGENT = []
        lines = open(file, 'r').readlines()
        for line in lines:
            self.__USER_AGENT.append(line.replace('\n',''))
    def urlopen(self, url):
        err_cnt = 0
        while 1:
            try:
                request = Request.Request(url, headers={'User-Agent':random.choice(self.__USER_AGENT)})
                html = Request.urlopen(request, timeout=self.__TIME_OUT).read()
            except:
                err_cnt += 1
                if err_cnt > 2 :
                    raise
            else:
                break
            time.sleep(1)
        return html

class ThreadPool:
    def __init__(self):
        self.__init_para(os.getcwd() + '\\ini.cfg', 'DEFAULT')
    def __init_para(self, file, section):
        cp = configparser.ConfigParser()
        cp.read(file, encoding='utf-8')
        self.__QSIZE = int(cp.get(section, 'TSIZE'))
        self.__THREAD_QUEUE = Queue(maxsize=-1)
        for i in range(self.__QSIZE):
            self.__THREAD_QUEUE.put('thread-' + str(i))
    def deco(self, func, *args, **kwargs):
        def job():
            func(*args, **kwargs)
            self.__THREAD_QUEUE.put(threading.currentThread().name)
        return job
    def execute(self, func, *args, **kwargs):
        thread_name = self.__THREAD_QUEUE.get()
        threading.Thread(target=self.deco(func, *args, **kwargs), name=thread_name).start()
    def wait(self):
        while self.__QSIZE != self.__THREAD_QUEUE.qsize():
            time.sleep(1)

class ProcessPool:
    def __init__(self):
        self.__init_para(os.getcwd() + '\\ini.cfg', 'DEFAULT')
    def __init_para(self, file, section):
        cp = configparser.ConfigParser()
        cp.read(file, encoding='utf-8')
        self.__QSIZE = int(cp.get(section, 'PSIZE'))
        self.__PROCESS_QUEUE = multiprocessing.Queue(maxsize=-1)
        for i in range(self.__QSIZE):
            self.__PROCESS_QUEUE.put('process-' + str(i))
    def deco(self, func, *args, **kwargs):
        @wraps(func)
        def job():
            func(*args, **kwargs)
            self.__PROCESS_QUEUE.put(multiprocessing.current_process().name)
        return job
    def execute(self, func, *args, **kwargs):
        process_name = self.__PROCESS_QUEUE.get()
        multiprocessing.Process(target=self.deco(func, *args, **kwargs), name=process_name).start()
    def wait(self):
        while self.__QSIZE != self.__PROCESS_QUEUE.qsize():
            time.sleep(1)

class Concurrent:
    def __init__(self, n_pro, func, *args):
        self.n_pro = n_pro
        self.q_in = multiprocessing.Queue(maxsize=-1)
        self.q_out = multiprocessing.Queue(maxsize=-1)
        self.counter = 0
        self.p_list = []
        for i in range(self.n_pro):
            p = multiprocessing.Process(func, self.q_in, self.q_out, *args, daemon=True)
            self.p_list.append(p)
            p.start()
    def put(self, input_list):
        for input in input_list:
            self.q_in.put(input)
            self.counter += 1
    def get(self):
        while self.check():
            try:
                output = self.q_out.get(timeout=1)
                self.counter -= 1
                return output
            except:
                continue
    def check(self):
        if sum([0 if p.alive() else 1 for p in self.p_list]) > 0:
            self.exit()
            raise('RuntimeError')
        return True
    def empty(self):
        return True if self.counter == 0 else False
    def overload(self):
        return True if self.counter >= self.n_pro else False
    def exit(self):
        self.q_out.close()
        for p in self.p_list:
            p.terminate()
            p.join()
    def __del__(self):
        self.exit()

def feature_processing(data, var_list , min_value=-np.inf, max_value=np.inf, fill_else=-9999, decimal=3):
    def limit(x):
        return x if x >= min_value and x <= max_value else fill_else
    for var in tqdm(var_list):
        data[var] = data[var].astype('float').apply(limit).round(decimal)

def target_processing(data, target_region, fill_na=0, fill_else=np.nan):
    for target in tqdm(list(target_region.keys())):
        data[target].fillna(fill_na,inplace=True)
        data.loc[~data.query(target_region[target]).index, target] = fill_else

