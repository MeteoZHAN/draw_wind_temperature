# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 20:32:15 2021

@author: ZHAN
"""

import glob
import numpy as np
import matplotlib.pyplot as plt
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs


files = glob.glob(r'C:\Users\ZHAN\Desktop\bbw_buqi\*.txt') # glob里的*相当于正则表达式的.*


'''判断各个txt行数是否一致
l=[]
for i in files:
    print(i)
    data = np.loadtxt(i)
    l.append(len(data))
'''

a = np.loadtxt(files[0])
path0 = r'D:\data\China_basic_map\广西.shp'
for i in range(8760):
    print(i)
    temp = np.zeros((81,21))
    row = -1
    for path in files:
        row = row + 1
        data = np.loadtxt(path)
        temp[row,:] = data[i,:]
        
    # 绘图   
    ax = plt.axes(projection = ccrs.PlateCarree())
    box = [106,111.3,20.8,23.5]
    ax.set_extent(box,crs=ccrs.PlateCarree())
    shp = list(shpreader.Reader(path0).geometries())
    ax.add_geometries(shp, ccrs.PlateCarree(), edgecolor='black',
                      facecolor='none',alpha=1,linewidth=0.5)   #加底图
    plt.scatter(temp[:,1],temp[:,0], marker = '.',c='k' )      #画站点
    
    t = (temp[:,13]+temp[:,15])/2 # 求平均值
    t = np.round(t,1)  # 保留一位小数
    u = v = np.zeros((len(temp)))
    for r in range(81):
        plt.text(temp[r,1],temp[r,0],str(t[r])) # 添加平均值
        # 分解风速到u v方向
        if temp[r,17] >= 360:
            u[r] = np.nan
            v[r] = np.nan
        elif temp[r,17] >= 0 and temp[r,17] < 90:
            u[r] = np.sin(temp[r,17]) * temp[r,8] * -1
            v[r] = temp[r,8] * np.cos(temp[r,17]) * -1
        elif temp[r,17] >= 90 and temp[r,17] < 180:
             u[r] = np.sin(180-temp[r,17]) * temp[r,8] * -1
             v[r] = temp[r,8] * np.cos(180 - temp[r,17])
        elif temp[r,17] >= 180 and temp[r,17] < 270:
             u[r] = np.sin(temp[r,17]-180) * temp[r,8]
             v[r] = temp[r,8] * np.cos(temp[r,17]-180)
        elif temp[r,17] >= 270 and temp[r,17] < 360:
             u[r] = np.sin(360-temp[r,17]) * temp[r,8]
             v[r] = temp[r,8] * np.cos(360-temp[r,17]) * -1
    plt.barbs(temp[:,1],temp[:,0],u,v,
              barb_increments = {'half':2,'full':4,'flag':20}) # zorder图层上下叠放位置，值越大越在上层
    
    # 保存图片
    fig = plt.gcf()
    fig.set_size_inches(20,15)
    name = str(int(temp[0,3])) +'-'+ str(int(temp[0,4])) + '-'+ str(int(temp[0,5])) + '-'+ str(int(temp[0,6]))
    plt.savefig('pic\\'+name +'.tif', bbox_inches='tight')
    plt.close()
