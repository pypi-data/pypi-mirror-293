import pandas as pd
import numpy as np
from dateutil.parser import parse
import os
#制动频率，整数，已化为百分数，返回值30代表30%
def bp_freq(dataframe):
    dataframe = dataframe.copy()
    return int(data[data['brake_stat']==1].shape[0]/data.shape[0]*100)
#加速频率，整数，单位%
def ap_freq(dataframe):
    dataframe = dataframe.copy()
    return int(data[data['power_stat']==1].shape[0]/data.shape[0]*100)
#初始soc
def init_soc(dataframe):
    data = dataframe.copy()
    return int(max(list(data['soc'])))
#行驶里程
def delta_dis(dataframe):
    data = dataframe.copy()
    max_dis=max(list(data['mileage']))*0.1
    min_dis=min(list(data['mileage']))*0.1
    return round(max_dis-min_dis,1)
#温度
def temp(dataframe):
    data = dataframe.copy()
    return data['T'].mean()
#平均速度单位km/h
def avg_v(dataframe):
    data = dataframe.copy()
    data['delta_time']=(data['daq_time'].apply(lambda x:parse(str(x)))).diff().dt.total_seconds()/60/60
    data['dis']=data['speed']*data['delta_time']*0.1
    time=(parse(str(data['daq_time'].max()))-parse(str(data['daq_time'].min()))).seconds/60/60
    if time != 0:
        return round(sum(list(data['dis'].dropna()))/time,2)
    else:
        return np.nan
#速度对时间积分计算里程,精度小数点后两位
def vt_dis(dataframe):
    data = dataframe.copy()
    data['delta_time']=(data['daq_time'].apply(lambda x:parse(str(x)))).diff().dt.total_seconds()/60/60
    data['dis']=data['speed']*data['delta_time']*0.1
    return round(sum(list(data['dis'].dropna())), 2)#2为小数点后2位
#soc变化量
def delta_soc(dataframe):
    data = dataframe.copy()
    max_soc=max(list(data['soc']))
    min_soc=min(list(data['soc']))
    return int(max_soc-min_soc)
#行驶时间,单位h
def delta_time(dataframe):
    data = dataframe.copy()
    return round((parse(str(data['daq_time'].max()))-parse(str(data['daq_time'].min()))).seconds/60/60,2)
#功能：处理时间
'''
    调用时传入片段dataframe，如返回是否休息，daq_time(dataframe).isrest
    例如：
    data=pd.DataFrame()
    data['daq_time']=pd.DataFrame(['20240830155100'])
    print(daq_time(data).weekday)输出值：5代表2024年8月30日为星期五
    print(daq_time(data).isrest输出值：0代表2024年8月30日为正常工作日，不休息
    
'''
class daq_time():
    time=None#起始时间
    weekday=None#星期几，数字1-7
    year=None#年
    month=None#月
    day=None#日
    hour=None#时
    minute=None#分
    second=None#秒
    begin_time=None#起始时刻近似到最近时刻，精度为半小时，如，16:37输出16.5,9:57输出10
    isrest=None#判断是否休息，考虑到节假日以及调休，0代表正常上班，1代表休息
    def __init__(self,dataframe):
        self.data=dataframe.copy()
        self.time=parse(str(data['daq_time'][0]))
        self.weekday=self.time.isoweekday()
        self.hour=self.time.hour
        self.minute=self.time.minute
        self.day=self.time.day
        self.month=self.time.month
        self.year=self.time.year
        self.second=self.time.second
        self.begin_time=self.round_to_nearest_half(self.hour+self.minute/60)
        self.isholiday=None
        #判断是否是周末
        if self.weekday in [6,7]:
            self.isweekend=True
        else:
            self.isweekend=False
        #节假日：不考虑寒暑假，因为有寒暑假的工作很少
        if self.year==2023:#2023年节假日及其调休
            if self.month==1:#一月节假日(只有一月有)
                if self.day in [1,2,21,22,23,24,25,26,27]:
                    self.isholiday=True#标记为假期
                if self.day in [28,29]:#调休上班
                    self.isholiday=False#标记为工作
        if self.year==2024:#24年节假日及其调休
            if self.month == 1:
                if self.day in [1]:
                    self.isholiday=True
            if self.month==2:
                if self.day in [10,11,12,13,14,15,16,17]:#年假
                    self.isholiday=True
                if self.day in [4,18]:
                    self.isholiday=False
        if self.isholiday!=None:
            if self.isweekend == True:#处理周末
                self.isrest=self.isweekend and self.isholiday#遇到节假日flase为假
            if self.isweekend == False:
                self.isrest=self.isweekend or self.isholiday
            self.isrest=int(self.isrest)
        else:
            self.isrest=int(self.isweekend)

    def round_to_nearest_half(self,value):
        return round(value * 2) / 2
#功能：计算能耗，单位KWh
'''
    调用时传入片段dataframe，energy(dataframe).cost
'''
class energy():
    cost=None
    def __init__(self,dataframe):
        data=dataframe.copy(deep=True)
        data['t_volt']=data['t_volt']*0.1#转换成V
        data['t_current']=data['t_current']*0.1#转换成A
        data['delta_time'] = (data['daq_time'].apply(lambda x: parse(str(x)))).diff().dt.total_seconds() / 60 / 60#小时
        data['energy']=data['t_volt']*data['t_current']*data['delta_time']/1000#能量块，单位KWH
        self.cost=round(sum(list(data['energy'].dropna())),2)
