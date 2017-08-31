# coding: utf-8

import tushare as ts
import pandas as pd

#全局变量

raw_data_dir = './raw_data/'

start = "2012-04-27"
end = "2017-08-23"

hs300 = ts.get_hs300s()
hs300['start'] = start
hs300['end'] = end
hs300.to_csv("config_stocklist.csv", index=False, header=False, columns=['code', 'start', 'end'])

itemlist = pd.read_csv("config_stocklist.csv", names=["code", "start","end"],dtype='str')

#获取素材列表并保存(在获取列表未变化时不运行该CELL)
format=lambda x: '%.6f' % x

for curIndex in itemlist.index:
    try:
       data=ts.get_k_data(itemlist.ix[curIndex, 'code'], start = itemlist.ix[curIndex, 'start'], end = itemlist.ix[curIndex, 'end'],autype='qfq')
       data.to_csv(raw_data_dir + itemlist.ix[curIndex, 'code']+'.csv', index = False, header=True)
    except Exception as e:
        print(itemlist.ix[curIndex, 'code'], e)
        continue
        


