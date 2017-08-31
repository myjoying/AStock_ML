# coding: utf-8

import pandas as pd
import numpy as np


class trade_statistics(object):
    '''
    交易策略统计数据
    '''
    def __init__(self):
        self.__trade_s = {}
        self.__mean_ins = 0
        self.__std_ins = 0
        self.__mean_dec = 0
        self.__std_dec = 0
        self.__count = 0
        self.__per_ins = 0
    
    #对股票策略数据进行统计，统计包括买卖时间，价格，交易次数，增长\亏损平均值，增长\亏损标准差，增长次数占比
    def start_statistic(self, code, t_strategy):
        if isinstance(t_strategy, pd.DataFrame)==False:
            print("parameter is not a DataFrame instance")
        tmp_data = pd.DataFrame(columns=['start', 'end', 'buy_price', 'sel_price', 'vary'])
        mean_ins = 0
        std_ins = 0
        mean_dec = 0
        std_dec = 0
        per_ins = 0
        t_buy_price = 0
        t_start = 0
        t_end = 0
        t_sel_price = 0
        t_vary = 0
        for i in range(np.size(t_strategy.index)):
            if (t_strategy.ix[i, 'buy_flag']==1) and (t_buy_price<=0):
                t_buy_price = t_strategy.ix[i, 'open'] #买价格
                t_start = t_strategy.index[i] #买时间
            if (t_strategy.ix[i, 'sel_flag']==1) and (t_buy_price > 0):
                t_end = t_strategy.index[i]  #卖时间
                t_sel_price = t_strategy.ix[i, 'open']  #卖价格
                t_vary = (t_sel_price - t_buy_price)/t_buy_price #价格变动
                tmp_data = pd.concat([tmp_data, \
                                     pd.DataFrame({'start':[t_start], 'end':[t_end], 'buy_price': [t_buy_price], 'sel_price':[t_sel_price], 'vary':[t_vary]})], \
                                    ignore_index = True)
                t_buy_price = 0
            
        vary_col = tmp_data['vary'] 
        mean_ins = vary_col[vary_col>0].mean() #增长平均值
        std_ins = vary_col[vary_col>0].std()  #增长标准差
        mean_dec = vary_col[vary_col<=0].mean() #亏损平均值
        std_dec = vary_col[vary_col<=0].std() #亏损标准差
        count = vary_col.count() #交易次数
        per_ins = vary_col[vary_col>0].count()/count #增长次数占比
            
        self.__trade_s[code] = {'data':tmp_data, \
        'statistics':{'count': count, 'mean_ins': mean_ins, 'std_ins':std_ins, \
                      'mean_dec':mean_dec, 'std_dec':std_dec, 'per_ins':per_ins }}
        
    #对所有股票交易数据进行统计
    def total_statistics(self):
        vary_col = pd.Series()
        for code in self.__trade_s:
            vary_col = pd.concat([vary_col, self.__trade_s[code]['data']['vary']])
        self.__mean_ins = vary_col[vary_col>0].mean()
        self.__std_ins = vary_col[vary_col>0].std()
        self.__mean_dec = vary_col[vary_col<=0].mean()
        self.__std_dec = vary_col[vary_col<=0].std()
        self.__count = vary_col.count()
        self.__per_ins = vary_col[vary_col>0].count() / self.__count
            
    def getStatistics(self):
        return self.__trade_s
    
    def getTradeCnt(self):
        return self.__count
    
    def getTradeInsMean(self):
        return self.__mean_ins
    
    def getTradeInsStd(self):
        return self.__std_ins
    
    def getTradeDecMean(self):
        return self.__mean_dec
    
    def getTradeDecStd(self):
        return self.__std_dec
    
    def getTradeInsPercent(self):
        return self.__per_ins
                
            
            
            


