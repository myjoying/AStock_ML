# coding: utf-8

import pandas as pd
import numpy as np
import talib as ta
import os as os
import matplotlib.pyplot as plt
from sklearn import linear_model

#全局变量
raw_data_dir = './raw_data/'
post_data_dir = './post_data/'

format=lambda x: '%.4f' % x

num = 0

reg = linear_model.LinearRegression()

#获取原始保存的素材raw_data
filelist = os.listdir(raw_data_dir)
DataDict = {}
for file in filelist:
    num = num+1
    if num!=1:
        continue
    
    key = file.split('.')[0]
    print(num, ' ', key)
    
    data = pd.read_csv(raw_data_dir + file, index_col = 0)
    data.sort_index(inplace=True)
    
    close = np.array(data['close'])
    high = np.array(data['high'])
    low = np.array(data['low'])
#    volume = np.array(data['volume'])
    data['SMA5'] = ta.SMA(close, timeperiod = 5)  #5日均线
#    data['SMA10'] = ta.SMA(close, timeperiod = 10)  #10日均线
#    data['SMA20'] = ta.SMA(close, timeperiod = 20)  #20日均线
#    data['SMA30'] = ta.SMA(close, timeperiod = 30)  #30日均线
#    data['SMA60'] = ta.SMA(close, timeperiod = 60)  #60日均线
    #upper, middle, lower = ta.BBANDS(close, matype=ta.MA_Type.T3)
#    data['DEMA5'] = ta.DEMA(close, timeperiod = 5)  #5日双指数平均
#    data['DEMA10'] = ta.DEMA(close, timeperiod = 10)  #10日双指数平均
#    data['DEMA30'] = ta.DEMA(close, timeperiod = 30)  #30日双指数平均
#    data['DEMA60'] = ta.DEMA(close, timeperiod = 60)  #60日双指数平均
    data['SAR'] = ta.SAR(high, low) #Stop And Reverse 买入和卖出指示抛物线指标
#    data['WMA'] = ta.WMA(close, timeperiod = 10)
#    data['MIDPOINT'] = ta.MIDPOINT(close, timeperiod = 10)
#    data['MIDPRICE'] = ta.MIDPRICE(high, low, timeperiod = 10)
#    data['MFI'] =  ta.MFI(high, low, close, volume,timeperiod = 10)/100
#    data['MOM10'] =  ta.MOM(close,timeperiod = 10)     #动量指标
#    data['MOM5'] =  ta.MOM(close,timeperiod = 5)     #动量指标
    
#    data['SMA5_P'] = (data['SMA5'] - data['SMA5'].shift(1))/data['SMA5']
#    data['SMA10_P'] = (data['SMA10'] - data['SMA10'].shift(1))/data['SMA10']
#    data['volume_P'] = (data['volume'] - data['volume'].shift(1))/data['volume']
    
#    data['MFI_P'] = (data['MFI'] - data['MFI'].shift(1))
    
#    data['MOM5_P'] = (data['MOM5'] - data['MOM5'].shift(1))
#    data['MOM10_P'] = (data['MOM10'] - data['MOM10'].shift(1))
    
    
#    data['change1'] = data['close'].shift(-1) - data['close']
#    data['change2'] = data['close'].shift(-2) - data['close']
#    data['change3'] = data['close'].shift(-3) - data['close']
#    data['b_change'] = 1  
#    data.ix[data['change1']>0.00, 'b_change'] = 2
           
#利用close价格计算趋势通道          
    RANGE = 30
    k = 0
    upper_b = 0
    down_b = 0
    trend_recalc = 5
    std_data = 0
    intercept = 0
    
#    f = open("log.txt",'w')
    data['trend'] = 0 #0--持平，负数--下跌累加，正数--上涨累加
    trend_flag = 0
    
    for i in range(RANGE, np.size(data.index)):
        if (i%RANGE==0) and (trend_recalc>3):
            trend_recalc = 0
            tmp_data = pd.Series(data.ix[i-RANGE:i, 'close'].values, index=range(i-RANGE,i))
#            tmp_data.sort_values(inplace=True)
#            min2 = tmp_data.head(n=2)
#            max1 = tmp_data.tail(n=1)
            
#            k = (min2.values[0]-min2.values[1])/(min2.index[0]-min2.index[1])
#            k = (tmp_data.values[4]-tmp_data.values[5])/(tmp_data.index[4]-tmp_data.index[5])
            X_train = np.array(tmp_data.index).reshape(-1,1)
            y_train = np.array(tmp_data.values)
            
            reg.fit(X_train,y_train)
            
            k = reg.coef_
            intercept = reg.intercept_
            if k<=0:
                if trend_flag<=0:
                    trend_flag = trend_flag -1
                else:
                    trend_flag = -1
            else:
                if trend_flag<=0:
                    trend_flag = 1
                else:
                    trend_flag = trend_flag + 1
            
#            down_b = min2.values[0] - k*min2.index[0]
#            upper_b =  max1.values[0] - k*max1.index[0]
            
            std_data = tmp_data.std()
            down_b = intercept - 2*std_data
            upper_b = intercept + 3*std_data
            
            
            
#            for j in tmp_data.index:
#                b = tmp_data[j] - k*j
#                if b>upper_b:
#                    upper_b = b
#                if b<down_b:
#                    down_b = b
        
        data.ix[i,'upper'] = k*i + upper_b 
        data.ix[i,'down'] = k*i + down_b
        data.ix[i,'trend'] = trend_flag
        data.ix[i,'k30'] = k
        data.ix[i,'std_data30'] = std_data
        data.ix[i,'intercept30'] = intercept
               
        
#        print('i=',i,'k=',k,file=f)
        
        if (data.ix[i,'close'] > data.ix[i,'upper']*1.01) or (data.ix[i,'close'] < data.ix[i,'down']*1.01):
            trend_recalc = trend_recalc+1
        #保存到文本
        data.to_csv(post_data_dir + str(key) +'.csv', index = True, header=True)
'''
    sec_RANGE = 10
    sec_k = 0
    sec_upper_b = 0
    sec_down_b = 0
    sec_trend_recalc = 5
    for i in range(sec_RANGE, np.size(data.index)):
        if (i%sec_RANGE==0) and (sec_trend_recalc>0):
            sec_trend_recalc = 0
            tmp_data = pd.Series(data.ix[i-sec_RANGE:i, 'close'].values, index=range(i-sec_RANGE,i))

            X_train = np.array(tmp_data.index).reshape(-1,1)
            y_train = np.array(tmp_data.values)
            
            reg.fit(X_train,y_train)
            
            sec_k = reg.coef_
            
#            down_b = min2.values[0] - k*min2.index[0]
#            upper_b =  max1.values[0] - k*max1.index[0]
            
            std_data = tmp_data.std()
            sec_down_b = reg.intercept_ - 2*std_data
            sec_upper_b = reg.intercept_ + 2*std_data
            
            
            
#            for j in tmp_data.index:
#                b = tmp_data[j] - k*j
#                if b>upper_b:
#                    upper_b = b
#                if b<down_b:
#                    down_b = b
        
        data.ix[i,'sec_upper'] = sec_k*i + sec_upper_b 
        data.ix[i,'sec_down'] = sec_k*i + sec_down_b
        
               
        
#        print('i=',i,'k=',k,file=f)
        
        if (data.ix[i,'close'] > data.ix[i,'sec_upper']*1.01) or (data.ix[i,'close'] < data.ix[i,'sec_down']*1.01):
            sec_trend_recalc = sec_trend_recalc+1        
'''
'''
    BBands_RANGE = 20    
    for i in range(BBands_RANGE, np.size(data.index)):
        tmp_data = pd.Series(data.ix[i-BBands_RANGE:i, 'close'].values, index=range(i-BBands_RANGE,i))
        std_data = tmp_data.std()
        data.ix[i,'B_upper'] = data.ix[i,'SMA20'] + 2.5*std_data 
        data.ix[i,'B_down'] = data.ix[i,'SMA20'] - 2*std_data 
         
'''     

    
    

#    ml_data = pd.DataFrame({"MOM10_0":data['MOM10'], 
#                            "MOM10_1":data['MOM10'].shift(1), 
#                            "MOM10_2":data['MOM10'].shift(2), 
#                            "MOM5_0":data['MOM5'], 
#                            "MOM5_1":data['MOM5'].shift(1), 
#                            "MOM5_2":data['MOM5'].shift(2),
#                            "a10" : data['MOM10']-2*data['MOM10'].shift(1)+data['MOM10'].shift(2),
#                            "a5" : data['MOM5']-2*data['MOM5'].shift(1)+data['MOM5'].shift(2),
#                            "MFI":data['MFI']/100, 
#                            "result":data['b_change']})
#    ml_data.applymap(format)
#    ml_data.ix[13:].to_csv(post_data_dir + 'ml_' + str(key) +'.csv', index = True, header=True)
'''
    data.index = pd.to_datetime(data.index)
    
    fig = plt.figure()
#    plt.subplot(211)
    ax1 = fig.add_subplot(111)
#    ax1.plot(data.index, data['MOM5'],marker='o',linestyle ='--',color = 'grey', markeredgecolor='blue',markerfacecolor ='none' )
    ax1.plot(data.index, data['SAR'],linestyle ='--',color = 'grey')
#    ax1.scatter(data.index, data['SAR'], c=data['b_change'])
    
    plt.xticks(rotation=45)
#    plt.legend()
    plt.title(key)
    
#    ax2 = ax1.twinx()
    ax1.plot(data['close'])
    ax1.plot(data['upper'],c='blue')
    ax1.plot(data['down'],c='blue')
    
#    ax1.plot(data['sec_upper'],c='yellow')
#    ax1.plot(data['sec_down'],c='yellow')

    ax1.plot(data['SMA5'],c='yellow')
#    ax1.plot(data['B_down'],c='yellow')

#    plt.subplot(212)
#    plt.scatter(X, data['MOM10'], c=data['b_change']) 
#    plt.title('MOM10')
'''
