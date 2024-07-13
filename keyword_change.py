#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 18:05:21 2024

@author: dongziyi
"""

import pandas as pd
import numpy as np
import math

root = 'D:/Yoren/数据分析/New'

df_2022 = pd.read_excel(root + '/' + '即食麦片SKU-销额计算结果.xlsx', sheet_name='MAT2305 SKU')
df_2023 = pd.read_excel(root + '/' + '即食麦片SKU-销额计算结果.xlsx', sheet_name='MAT2405 SKU')

df_output = pd.read_excel(root + '/' + '结果.xlsx')

keywords = df_output['keywords'].to_list()

def calculate_sales_sum(df, df_output, keywords_list, column, year):
    for keywords in keywords_list:
        # 拆分关键词，处理“AorBorC”格式
        # individual_keywords = keywords.split('or')
        individual_keywords = keywords.split('|')
        
        
        # 对于每个独立关键词，更新标记列
        for keyword in individual_keywords:
            df[keyword + '_label'] = df['标题&SKU&口味1&原料&口味2'].apply(lambda x: 1 if keyword in x else 0)
        
        # 计算拆分后关键词的销售额总和
        label_columns = [keyword + '_label' for keyword in individual_keywords]
        # df['total_sales'] = df[label_columns].sum(axis=1)
        sales_sum = df[df[label_columns].sum(axis=1) > 0]['销售额'].sum()
        
        # 更新输出DataFrame
        df_output.loc[df_output[column] == keywords, year] = sales_sum
        
calculate_sales_sum(df_2022, df_output, keywords, 'keywords', '2022销售额')
calculate_sales_sum(df_2023, df_output, keywords, 'keywords', '2023销售额')

df_output.to_excel(root + '/' + '结果计算.xlsx')