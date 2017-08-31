# coding: utf-8

import pandas as pd
import numpy as np
import os as os
import matplotlib.pyplot as plt
import trade_statistics as tst

#全局变量
raw_data_dir = './raw_data/'
post_data_dir = './post_data/'

format=lambda x: '%.4f' % x

num = 0
next_op = 0 #0--无操作，1--买，2--卖
pos = 0
n_trend = 0

#获取原始保存的素材raw_data
filelist = os.listdir(post_data_dir)
DataStatistic = tst.trade_statistics()

for file in filelist:
    key = file.split('.')[0]
    data = pd.read_csv(post_data_dir + file, index_col = 0)
    
    num = num+1
#    if num>=100:
#        continue
    
    print(num, key)
    
    data.sort_index(inplace=True)
    open = np.array(data['open'])
    close = np.array(data['close'])
#    high = np.array(data['high'])
#    low = np.array(data['low'])
#    volume = np.array(data['volume'])
    sar = np.array(data['SAR'])
    upper = np.array(data['upper'])
    down = np.array(data['down'])
    sma5 = np.array(data['SMA5'])
    
    data['buy_flag']=0
    data['sel_flag']=0
    
    for i in range(np.size(data.index)):
        
        if next_op==1:
            data.ix[i,'buy_flag']= 1
            next_op = 0

                       
        if next_op==2:
            data.ix[i,'sel_flag']= 1
            next_op = 0
            
#        cur_trend = data.ix[i, 'trend']
#        if (cur_trend<=-2) and (n_trend>-2):
#            next_op = 2
#        n_trend = cur_trend
        
        cur_pos = 0
        if (sma5[i]>upper[i]):
            cur_pos = 1
            if pos!=1:
                next_op = 1
        elif (sma5[i]<down[i]):
            cur_pos = 3
            if pos != 3:
                next_op = 2
        else:
            cur_pos = 2
        pos = cur_pos


#计算收益率                    
#    buy_price = 0
#    vary_precent = 0
#    data['vary_precent'] = 0            
#    for i in range(np.size(data.index)):
#        if buy_price>0:
#            vary_precent = (close[i] - buy_price)/buy_price
#            if data.ix[i,'sel_flag']==1:
#                vary_precent = (open[i] - buy_price)/buy_price
#            data.ix[i,'vary_precent'] = vary_precent
#                   
#        if (data.ix[i,'buy_flag']== 1) and (buy_price<=0.0001):
#            buy_price = open[i]
#        if data.ix[i,'sel_flag']==1:
#            buy_price = 0
            
    DataStatistic.start_statistic(key, data)

DataStatistic.total_statistics()

AA = DataStatistic.getStatistics() 
print(AA)    
print('cnt:', DataStatistic.getTradeCnt())
print('DecMean:', DataStatistic.getTradeDecMean())
print('DecStd:', DataStatistic.getTradeDecStd())
print('InsMean:', DataStatistic.getTradeInsMean())
print('InsStd:', DataStatistic.getTradeInsStd())
print('InsPercent:', DataStatistic.getTradeInsPercent())
        
        
    

    #保存到文本
    

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

#    data.index = pd.to_datetime(data.index)
#    
#    fig = plt.figure()
##    plt.subplot(211)
#    ax1 = fig.add_subplot(111)
##    ax1.plot(data.index, data['MOM5'],marker='o',linestyle ='--',color = 'grey', markeredgecolor='blue',markerfacecolor ='none' )
#    ax1.plot(data.index, data['SMA5'],linestyle ='--',color = 'grey')
#    ax1.plot(data.index,data['close'])
#    ax1.plot(data.index,data['upper'],c='blue')
#    ax1.plot(data.index,data['down'],c='yellow')
#    
#    ax1.scatter(data.index, data['buy_flag'], c='red')
#    ax1.scatter(data.index, data['sel_flag'], c='black')
#    
#    plt.xticks(rotation=45)
##    plt.legend()
#    plt.title(key)
#    
#    ax2 = ax1.twinx()
#    ax2.plot(data.index,data['vary_precent'],c='red')

#    plt.subplot(212)
#    plt.scatter(X, data['MOM10'], c=data['b_change']) 
#    plt.title('MOM10')


