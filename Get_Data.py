# coding: utf-8

import tushare as ts
import pandas as pd

#全局变量
itemlist = pd.read_csv("config_stocklist.csv", names=["ID", "start","end","Name"],dtype='str')
raw_data_dir = './raw_data/'


#获取素材列表并保存(在获取列表未变化时不运行该CELL)
format=lambda x: '%.6f' % x

for curIndex in itemlist.index:
   data=ts.get_h_data(itemlist.ix[curIndex, 'ID'], start = itemlist.ix[curIndex, 'start'], end = itemlist.ix[curIndex, 'end'])
   data.to_csv(raw_data_dir + itemlist.ix[curIndex, 'ID']+'.csv', index = True, header=True)


