# coding: utf-8

import pandas as pd
import numpy as np
import talib as ta
import os as os

#全局变量
raw_data_dir = './raw_data/'
post_data_dir = './post_data/'

#获取原始保存的素材raw_data
filelist = os.listdir(raw_data_dir)
DataDict = {}
for file in filelist:
    key = file.split('.')[0]
    DataDict[key] = pd.read_csv(raw_data_dir + file, index_col = 0)

format=lambda x: '%.4f' % x

#计算指标
for key in DataDict:
    data = DataDict[key]
    data.sort_index(inplace=True)
    close = np.array(data['close'])
    high = np.array(data['high'])
    low = np.array(data['low'])
    volume = np.array(data['volume'])
    data['SMA5'] = ta.SMA(close, timeperiod = 5)  #5日均线
    data['SMA10'] = ta.SMA(close, timeperiod = 10)  #10日均线
    data['SMA30'] = ta.SMA(close, timeperiod = 30)  #30日均线
    data['SMA60'] = ta.SMA(close, timeperiod = 60)  #60日均线
    #upper, middle, lower = ta.BBANDS(close, matype=ta.MA_Type.T3)
    data['DEMA5'] = ta.DEMA(close, timeperiod = 5)  #5日双指数平均
    data['DEMA10'] = ta.DEMA(close, timeperiod = 10)  #10日双指数平均
    data['DEMA30'] = ta.DEMA(close, timeperiod = 30)  #30日双指数平均
    data['DEMA60'] = ta.DEMA(close, timeperiod = 60)  #60日双指数平均
    data['SAR'] = ta.SAR(high, low)
    data['WMA'] = ta.WMA(close, timeperiod = 10)
    data['MIDPOINT'] = ta.MIDPOINT(close, timeperiod = 10)
    data['MIDPRICE'] = ta.MIDPRICE(high, low, timeperiod = 10)
    data['MFI'] =  ta.MFI(high, low, close, volume,timeperiod = 10)
    data['MOM10'] =  ta.MOM(close,timeperiod = 10)     #动量指标
    data['MOM5'] =  ta.MOM(close,timeperiod = 5)     #动量指标
    data['change1'] = data['close'].shift(-1) - data['close']
    data['change2'] = data['close'].shift(-2) - data['close']
    data['change3'] = data['close'].shift(-3) - data['close']
    data['b_change'] = 1  
    data.ix[((data['change1']>0.01) | (data['change2']>0.01)|(data['change3']>0.01)), 'b_change'] = 2
    

    #保存到文本
    data.to_csv(post_data_dir + str(key) +'.csv', index = True, header=True)
    

    ml_data = pd.DataFrame({"MOM10_0":data['MOM10'], 
                            "MOM10_1":data['MOM10'].shift(1), 
                            "MOM10_2":data['MOM10'].shift(2), 
                            "MOM5_0":data['MOM5'], 
                            "MOM5_1":data['MOM5'].shift(1), 
                            "MOM5_2":data['MOM5'].shift(2),
                            "a10" : data['MOM10']-2*data['MOM10'].shift(1)+data['MOM10'].shift(2),
                            "a5" : data['MOM5']-2*data['MOM5'].shift(1)+data['MOM5'].shift(2),
                            "MFI":data['MFI']/100, 
                            "result":data['b_change']})
    ml_data.applymap(format)
    ml_data.ix[13:].to_csv(post_data_dir + 'ml_' + str(key) +'.csv', index = True, header=True)


