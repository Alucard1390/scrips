# %%
import os
import pandas as pd
import re
import numpy as np
from datetime import datetime,timedelta

# %%
now = datetime.now()

first_day_of_current_month = now.replace(day=1)
last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
 
previous_year = last_day_of_previous_month.year
previous_month = last_day_of_previous_month.month
 
file_name_month = f"{previous_year}年{previous_month}月"
print(file_name_month)

# %%
itemList = ["塞德思","灵的融","希纳露","百热朗","健眠计划","S+","琵力消","VL"]
def tag_add(itemName,itemLists):
    for item in itemLists:
        if item in itemName:
            return item
        else:
            continue
    return itemName

# %%
bilibili_list = [730603253025,730903103301,730740810652]
def bilibili_taoke_divide(sku_id,file_name):
    if sku_id in [730603253025,730903103301,730740810652]:
        return "B站"
    else:
        return "taoke"

# %%
file_dir = "C:\\盐野义\\月报\\"+file_name_month+"\\淘客数据"
csv_list=os.listdir(file_dir)
taoke_data = pd.read_csv("C:/盐野义/月报/"+file_name_month+"/淘客数据/"+csv_list[0])
#taoke_data["渠道"] = taoke_data["商品ID"].apply(lambda x:bilibili_taoke_divide(x,bilibili_list=bilibili_list,file_name=csv_list[0]))
taoke_data["文件名"] = csv_list[0]
taoke_data["统计时间"] = datetime.strptime(csv_list[0][:10],"%Y-%m-%d")
#taoke_data["渠道"] = "B站" if taoke_data["商品ID"] in bilibili_list and ("定向计划".isin(taoke_data["文件名"]) or "自主推广-商品维度-推广概览-数据分布" in taoke_data["文件名"]) else "taoke"

for csvs in csv_list[1:]:    
    taoke_data_sub = pd.read_csv("C:/盐野义/月报/"+file_name_month+"/淘客数据/"+csvs)
    #taoke_data_sub["渠道"] = taoke_data["商品ID"].apply(lambda x:bilibili_taoke_divide(x,bilibili_list=bilibili_list,file_name=csvs))
    taoke_data_sub["文件名"] = csvs
    taoke_data_sub["统计时间"] = datetime.strptime(csvs[:10],"%Y-%m-%d")
    #taoke_data_sub["渠道"] = "B站" if int(taoke_data["商品ID"]) in bilibili_list and ("定向计划" in taoke_data["文件名"] or "自主推广-商品维度-推广概览-数据分布" in taoke_data["文件名"]) else "taoke"
    taoke_data = pd.concat([taoke_data,taoke_data_sub],axis=0,ignore_index=True)
taoke_data["商品别名"] = taoke_data["商品名称"].astype(str).apply(lambda x:tag_add(x,itemLists=itemList))


# %%
taoke_data["渠道"] = taoke_data.apply(lambda row:bilibili_taoke_divide(sku_id=row["商品ID"],file_name=row["文件名"]),axis=1)

# %%
taoke_data.to_excel(file_dir+"\\淘客数据raw_data.xlsx",index = False)

# %%
taoke_data_pivot = taoke_data.pivot_table(values=["点击量(即进店量)","付款人数","付款支出费用","付款金额"],index=["渠道","商品别名"],aggfunc=[np.sum])

# %%
taoke_data_pivot.to_excel(file_dir+"\\淘客数据总结.xlsx")


