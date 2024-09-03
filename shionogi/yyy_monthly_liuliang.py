# %%
import pandas as pd
import os
from datetime import datetime

this_month = str(datetime.now().year)+"年"+str(datetime.now().month-1)+"月"



# %%
with pd.ExcelWriter("D:/盐野义/月报/"+this_month+"/主商品流量.xlsx") as wt:   
    for item in ["灵的融","希纳露"]:
        linderong_xls_list=os.listdir("D:/盐野义/月报/"+this_month+"/灵的融流量")
        linderong_liuliang_data = pd.read_excel(io="D:/盐野义/月报/"+this_month+"/灵的融流量/"+linderong_xls_list[0],skiprows=5,engine="xlrd")

        # %%
        for linderong_xlss in linderong_xls_list[1:]:
            linderong_liuliang_data_sub = pd.read_excel(io="D:/盐野义/月报/"+this_month+"/灵的融流量/"+linderong_xlss,skiprows=5,engine="xlrd")
            linderong_liuliang_data = pd.concat([linderong_liuliang_data,linderong_liuliang_data_sub],axis=0,ignore_index=True)

        # %%
        linderong_liuliang_data_count = linderong_liuliang_data[linderong_liuliang_data["三级来源"].isin(["智能场景(原万相台)","精准人群推广(原引力魔方)","关键词推广(原直通车)"])]

        # %%
        linderong_liuliang_data_count["访客数"]=linderong_liuliang_data_count["访客数"].apply(lambda x:str(x).replace(",",""))
        linderong_liuliang_data_count["浏览量"]=linderong_liuliang_data_count["浏览量"].apply(lambda x:str(x).replace(",",""))
        linderong_liuliang_data_count["支付金额"]=linderong_liuliang_data_count["支付金额"].apply(lambda x:str(x).replace(",",""))
        linderong_liuliang_data_count["支付买家数"]=linderong_liuliang_data_count["支付买家数"].apply(lambda x:str(x).replace(",",""))
        linderong_liuliang_data_count["支付件数"]=linderong_liuliang_data_count["支付件数"].apply(lambda x:str(x).replace(",",""))
        linderong_liuliang_data_count = linderong_liuliang_data_count.astype({"访客数":"int64"
            ,"浏览量":"int64"
            ,"支付金额":"float64"
            ,"支付买家数":"int64"
            ,"支付件数":"int64"
                                    })


        # %%
        linderong_liuliang_data_count.pivot_table(values=["支付金额"],index="三级来源")
        linderong_liuliang_data_count.to_excel(wt,sheet_name=item,index=False)


