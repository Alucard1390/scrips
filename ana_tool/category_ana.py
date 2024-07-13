# %%
import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine

# %%
def set_bin(top_limit:int,max_limit:int,gap_num:int)->list:
    '''
    设置价格带的分层\n
    args:
        top_limit:价格带的最高统计数值
        max_limit:价格带的最高数值
        gap_num:价格带的范围大小
    return:
        bin_list->价格带的list返回给pands的cut函数使用
    '''
    bin_list = list(range(0,top_limit,gap_num))
    bin_list.append(max_limit)
    return bin_list


def init_category_df(gap_num:int,excelFileName:str=None,sheet_name:str=None,wps_df:pd.DataFrame=None,category_dict:dict=None,obj_to_date:str=None,top_limit:int=1000)->pd.DataFrame:
    '''
    读取原文件\n
    args:
        excelFileName:原文件路径
        sheet_name:数据所在sheet名
        gap_num:价格带的设置范围
        category_dict:{"category_level":类目等级->str,"category_name":类目详细的列表->list}
        obj_to_date:将指定列的格式转为日期
        top_limit:价格带的最高统计数值
    return:
        添加了销售年|销售月|价格带的dataframe
    '''
    if excelFileName is not None:
        if sheet_name is None:
            df = pd.read_excel(io=excelFileName)
        elif sheet_name is not None:
            df = pd.read_excel(io=excelFileName,sheet_name=sheet_name)
    elif wps_df is not None:
        df = wps_df.copy()
    else:
        raise ValueError("无效的df")
    if category_dict is None:
        if obj_to_date is None or obj_to_date=="":
            df = df
        else:
            #df = pd.read_excel(io=excelFileName,sheet_name=sheet_name)
            df["月"]=pd.to_datetime(df[obj_to_date],format="%Y-%m-%d")
            df["年"]=df["月"].dt.year
    else:
        if obj_to_date is None or obj_to_date=="":
            #df = pd.read_excel(io=excelFileName,sheet_name=sheet_name)
            df = df[df[category_dict["category_level"]].isin(category_dict["category_name"])]
        else:
            #df = pd.read_excel(io=excelFileName,sheet_name=sheet_name)
            df = df[df[category_dict["category_level"]].isin(category_dict["category_name"])]
            df["月"]=pd.to_datetime(df[obj_to_date],format="%Y-%m-%d")
            df["年"]=df["月"].dt.year
    df["价格带"] = pd.cut(df["价格"],bins=set_bin(int(top_limit),int(df["价格"].max()),gap_num=gap_num),precision=0)
    return df

def salesPivotPercent(df:pd.DataFrame,index:str,value:str,column:str,agg_func_list:list)->pd.DataFrame:
    '''
    生成透视表\n
    args:
        df:需透视的df
        index:结果的行
        column:结果的列
        value:聚合对象
        agg_func_list:环比聚合的list例:[2021,2022,2023]则按左侧年份环比
    return:
        聚合后并生成环比|比例的df(去除了other/其他/空)
    '''
    pivot_table = pd.pivot_table(df,index=index,values=value,columns=column,aggfunc=[np.sum])
    categorySalePivotTable = pivot_table["sum"].copy()
    for saleYear in agg_func_list:
        try:
            categorySalePivotTable[str(saleYear)+"环比"]=((categorySalePivotTable[saleYear]-categorySalePivotTable[saleYear-1])/categorySalePivotTable[saleYear-1])
        except:
            pass
    for saleYear in agg_func_list:    
        categorySalePivotTable[str(saleYear)+value+"占比"]=pd.to_numeric((categorySalePivotTable[saleYear]/np.sum(categorySalePivotTable[saleYear])))
    categorySalePivotTable = categorySalePivotTable.sort_values(by=agg_func_list[-1],ascending=False)
    for table_index in categorySalePivotTable.index.tolist():
        if table_index in ["other/其他","选择other/其他","other/其它","others",""," "] or table_index==None:
            categorySalePivotTable.drop(index=table_index,inplace=True)
        else:
            continue
    return categorySalePivotTable

def separate_brand(df_to_separate:pd.DataFrame,num_of_top:int):
    '''
    根据某一个聚合结果分离top_index,并分离业绩增长和变差的index\n
    args:
        df_to_separate:需要分离的df
        num_of_top:top的数量,20则选择top20
    return:
        返回一个top|业绩增长|业绩减少字典
    '''
    separated_brand_dict = {}
    topbrand = df_to_separate.index.tolist()[:num_of_top]
    urerubrand = [x for x in df_to_separate[df_to_separate["2023环比"]>0].index.tolist() if x in topbrand]
    urenaibrand = [y for y in topbrand if y not in urerubrand]
    separated_brand_dict["topbrand"]=topbrand
    separated_brand_dict["urerubrand"]=urerubrand
    separated_brand_dict["urenaibrand"]=urenaibrand
    return separated_brand_dict

def top20branddf_output(df_for_choose,topdict):
    return df_for_choose[df_for_choose["品牌"].isin(topdict["topbrand"])]

def urerubranddf_output(df_for_ureru,urerudict):
    return df_for_ureru[df_for_ureru["品牌"].isin(urerudict["urerubrand"])]

def urenaibranddf_output(df_for_urenai,urenaidict):
    return df_for_urenai[df_for_urenai["品牌"].isin(urenaidict["urerubrand"])]

def get_firstnum_from_string(string_to_clean):
    pattern = r"\d+(.\d+)?"
    matcher = re.match(pattern=pattern,string=string_to_clean)
    if matcher:
        return matcher.group()
    else:
        return string_to_clean
    
def change_tags(string_to_tag,tag_list:list):
    for tag in tag_list:
        if tag in string_to_tag:
            return tag
        else:
            return "その他"

def price_layer(price,price_top,price_gap):
    if price>price_top:
            priceLayer=str(price_top)+"-"
    else:
        for p in range(0,price_top,price_gap):
            if price>=p:
                priceLayer=str(p)+"-"+str(p+price_gap)
            else:
                continue
    return priceLayer

def count_words(column_lable_list:list,df_for_count:pd.DataFrame,column_num:int,count_target_column_num:int,agg_target_num:int=None):
    count_dict = {}
    for count_lable in column_lable_list:
        count_dict[str(count_lable)]={}
    for i in range(1,len(df_for_count)):
        fenci_column = str(df_for_count.iloc[i,column_num])
        fenci_list = df_for_count.iloc[i,count_target_column_num]
        if agg_target_num ==None:
            count_num = 1
        else:    
            count_num = df_for_count.iloc[i,agg_target_num]
        for j in fenci_list:
            if j in count_dict[fenci_column].keys():
                count_dict[fenci_column][j]+=count_num
            else:
                count_dict[fenci_column][j]=count_num

def df_to_sql(df_to_dwh,dwh_list):
    username = "root"
    password = "9518llhh731X"
    host = "localhost"
    port = 3306
    database = "dwh"
    charset = "utf8mb4"
    connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset={charset}'
    conn = create_engine(connection_string)
    pd.io.sql.to_sql(df_to_dwh,dwh_list,con=conn)
    return


