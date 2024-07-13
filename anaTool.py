import pandas as pd
import numpy as np

def salesVolumnPercent(df:pd.DataFrame,index:str,value:str)->pd.DataFrame:
    pivot_table = pd.pivot_table(df,index=[index],values=[value],aggfunc=[np.sum])
    pivot_table["总销售额"]=np.sum(pivot_table["sum"]["销售额"])
    pivot_table["合计百分比"]=(pivot_table["sum"]["销售额"]/pivot_table["总销售额"]).apply(lambda x: '{:.2%}'.format(x))
    pivot_table = pivot_table.sort_values(by="合计百分比",ascending=False)
    return pivot_table

def changeObjToDate(dfTochange:pd.DataFrame,column:str,format:str)->pd.DataFrame:
    dfTochange[column]=pd.to_datetime(dfTochange[column],format=format)
    return dfTochange