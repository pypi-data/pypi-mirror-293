# -*- coding: utf-8 -*-
from util import LogHander,UrlHander,ThreadPool
from queue import Queue
import configparser
import re, os

class StockBase(LogHander, UrlHander):
    def __init__(self):
        LogHander.__init__(self)
        UrlHander.__init__(self)
        self.__init_para(os.getcwd() + '\\ini.cfg', 'DEFAULT')
        self.load_stock_list()
    def __init_para(self, file, section):
        cp = configparser.ConfigParser()
        cp.read(file, encoding='utf-8')
        self.__BASE_PATH = cp.get(section, 'DATA_PATH')
        if not os.path.exists(self.__BASE_PATH):
            os.mkdir(self.__BASE_PATH)
        self.__STOCK_LIST = cp.get(section, 'STOCK_LIST')
        self.__STOCK_LIST_FILE = self.__BASE_PATH + '/' + self.__STOCK_LIST
    def get_stock_list(self):
        self.logging('正在获取股票代码清单...')
        url = 'http://quotes.money.163.com/hs/service/diyrank.php?host=http://quotes.money.163.com/hs/service/diyrank.php&page=0&query=STYPE:EQA&fields=NO,SYMBOL,NAME,PRICE,PERCENT,UPDOWN,FIVE_MINUTE,OPEN,YESTCLOSE,HIGH,LOW,VOLUME,TURNOVER,HS,LB,WB,ZF,PE,MCAP,TCAP,MFSUM,MFRATIO.MFRATIO2,MFRATIO.MFRATIO10,SNAME,CODE,ANNOUNMT,UVSNEWS&sort=PERCENT&order=desc&count=10000&type=query'
        html = self.urlopen(url)
        stock_list = re.compile('"SYMBOL":"(\d*?)"'.encode('utf-8')).findall(html)
        for i in range(len(stock_list)):
            stock_list[i] = stock_list[i].decode('utf-8')
        stock_data = '\n'.join(stock_list)
        open(self.__STOCK_LIST_FILE, 'w').write(stock_data)
        self.logging('获取股票代码清单完成！')
    def load_stock_list(self):
        self.__STOCK_QUEUE = Queue(maxsize=-1)
        self.__STOCK_QUEUE_SUCCESS = Queue(maxsize=-1)
        self.__STOCK_QUEUE_FAILED = Queue(maxsize=-1)
        if not os.path.exists(self.__STOCK_LIST_FILE):
            self.get_stock_list()
        file = open(self.__STOCK_LIST_FILE)
        while 1:
            stock_id = file.readline().replace('\n','')
            if not stock_id:
                break
            self.__STOCK_QUEUE.put(stock_id)
        file.close()
    def get(self):
        stock_id = self.__STOCK_QUEUE.get()
        return stock_id
    def put(self, stock_id, error=False):
        if error:
            self.__STOCK_QUEUE_FAILED.put(stock_id)
        else:
            self.__STOCK_QUEUE_SUCCESS.put(stock_id)
    def empty(self):
        return self.__STOCK_QUEUE.empty()
    def move(self):
        while not self.__STOCK_QUEUE_FAILED.empty():
            self.__STOCK_QUEUE.put(self.__STOCK_QUEUE_FAILED.get())
    def update(self):
        self.get_stock_list()
        self.load_stock_list()
    def reset(self):
        self.load_stock_list()
    def normalwork(self, func, *args, **kwargs):
        while not self.empty():
            stock_id = self.get()
            func(stock_id, *args, **kwargs)
        self.move()
    def multithread(self, func, *args, **kwargs):
        pool = ThreadPool()
        while not self.empty():
            stock_id = self.get()
            pool.execute(func, stock_id, *args, **kwargs)
        pool.wait()
        self.move()
    def work(self, method, func, *args, **kwargs):
        if method == 1:
            self.normalwork(func, *args, **kwargs)
        elif method == 2:
            self.multithread(func, *args, **kwargs)
    def stat(self):
        self.logging(('股票总数:\t' + str(self.__STOCK_QUEUE_SUCCESS.qsize() + self.__STOCK_QUEUE.qsize())))
        self.logging(('已完成数量:\t' + str(self.__STOCK_QUEUE_SUCCESS.qsize())))
        self.logging(('未完成数量:\t' + str(self.__STOCK_QUEUE.qsize())))

class Crawler_wangyi(StockBase):
    def __init__(self):
        StockBase.__init__(self)
        self.__init_para(os.getcwd() + '\\ini.cfg', 'DEFAULT')
        self.load_stock_list()
    def __init_para(self, file, section):
        cp = configparser.ConfigParser()
        cp.read(file, encoding='utf-8')
        self.__BASE_PATH = cp.get(section, 'DATA_PATH')
        if not os.path.exists(self.__BASE_PATH):
            os.mkdir(self.__BASE_PATH)
        self.__DATA_PATH = self.__BASE_PATH + '/wangyi'
        if not os.path.exists(self.__DATA_PATH):
            os.mkdir(self.__DATA_PATH)
    def __get_stock_data(self, stock_id, year, season, filename):
        url = 'http://quotes.money.163.com/trade/lsjysj_' + stock_id + '.html?year=' + year + '&season=' + season
        html = self.urlopen(url)
        pattern = re.compile('<table class="table_bg001 border_box limit_sale">(.*?)</table>'.encode('utf-8'),re.S)
        text = pattern.findall(html)[0]
        pattern = re.compile('<td[^>]*?>(.*?)</td>'.encode('utf-8'), re.S)
        stock_data1 = pattern.findall(text)
        for i in range(len(stock_data1)):
            stock_data1[i] = stock_data1[i].decode('utf-8')
        stock_data2 = []
        #日期,开盘价,最高价,最低价,收盘价,涨跌额,涨跌幅,成交量,成交金额,振幅,换手率
        for i in range(0,len(stock_data1),11):
            line = '|'.join(stock_data1[i:(i+11)]).replace(',','').split('|')
            #日期,开盘价,最高价,最低价,收盘价,成交量,成交金额,换手率
            data = ','.join([line[0], line[1], line[2], line[3], line[4], line[7], line[8], line[10]])
            stock_data2.append(data)
        if not stock_data2:
            return
        stock_data = '\n'.join(stock_data2[::-1])
        open(filename, 'a').write(stock_data + '\n')
    def __get_stock_all(self, stock_id, start_year, end_year):
        filename = self.__DATA_PATH + '/' + stock_id + '.dat'
        open(filename, 'w').write('datatime,open_price,max_price,min_price,close_price,volume,amount,change_rate\n')
        try:
            for year in range(start_year, end_year+1):
                for season in range(1,5):
                    self.__get_stock_data(stock_id, str(year), str(season), filename)
        except:
            self.put(stock_id, error=True)
            self.logging(stock_id + ' => ' + filename + ' Failed!', error=True)
        else:
            self.put(stock_id)
            self.logging(stock_id + ' => ' + filename + ' Success!')
    def run(self, method=1, start_year=2010, end_year=2025):
        self.work(method, self.__get_stock_all, start_year, end_year)

class Crawler_sohu(StockBase):
    def __init__(self):
        StockBase.__init__(self)
        self.__init_para(os.getcwd() + '\\ini.cfg','DEFAULT')
    def __init_para(self, file, section):
        cp = configparser.ConfigParser()
        cp.read(file, encoding='utf-8')
        self.__BASE_PATH = cp.get(section, 'DATA_PATH')
        if not os.path.exists(self.__BASE_PATH):
            os.mkdir(self.__BASE_PATH)
        self.__DATA_PATH = self.__BASE_PATH + '/sohu'
        if not os.path.exists(self.__DATA_PATH):
            os.mkdir(self.__DATA_PATH)
    def __get_stock_data(self, stock_id, start_dt, end_dt, filename):
        start_dt = start_dt.replace('-', '')
        end_dt = end_dt.replace('-', '')
        url = 'http://q.stock.sohu.com/hisHq?code=cn_' + stock_id + '&start=' + start_dt + '&end=' + end_dt + '&stat=1&order=D&period=d&callback=historySearchHandler&rt=jsonp'
        html = self.urlopen(url)
        #日期,开盘,收盘,涨跌额,涨跌幅,最低,最高,成交量,成交金额,换手率
        stock_data1 = re.compile('\[("\d{4}-\d{2}-\d{2}"[^\]]*?)\]'.encode('utf8')).findall(html)
        stock_data2 = []
        for i in range(len(stock_data1)):
            line = stock_data1[i].decode('utf-8').replace('"', '').replace('%', '').split(',')
            #日期,开盘价,最高价,最低价,收盘价,成交量,成交金额,换手率
            data = ','.join([line[0], line[1], line[6], line[5], line[2], line[7], line[8], line[9]])
            stock_data2.append(data)
        stock_data = '\n'.join(stock_data2[::-1])
        open(filename,'a').write(stock_data)
    def __get_stock_all(self, stock_id, start_dt, end_dt):
        filename = self.__DATA_PATH + '/' + stock_id + '.dat'
        open(filename, 'w').write('datatime,open_price,max_price,min_price,close_price,volume,amount,change_rate\n')
        try:
            self.__get_stock_data(stock_id, start_dt, end_dt, filename)
        except:
            self.put(stock_id, error=True)
            self.logging(stock_id + ' => ' + filename + ' Failed!', error=True)
        else:
            self.put(stock_id)
            self.logging(stock_id + ' => ' + filename + ' Success!')
    def run(self, method=1, start_dt='1990-01-01', end_dt='2099-12-31'):
        self.work(method, self.__get_stock_all, start_dt, end_dt)

def Crawler(src):
    try:
        base_class = globals()['Crawler_%s' % src]
        class der_class(base_class):
            def __init__(self):
                base_class.__init__(self)
    except:
        raise Exception('数据源不存在!')
    return der_class()
