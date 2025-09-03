# %%
import os
import pandas as pd
import re
from datetime import datetime,timedelta
import promutil as pu

# %%
brands = ["alinamin","雪肌精","beme"]
for brand in brands:
    original_file_path = "D:/推广/"+brand+"/日报/每日数据源"
    zipped_file_path = "D:/推广/"+brand+"/日报/每日数据源解压"
    cleaned_file_path = "D:/推广/"+brand+"/日报"
    excel_output_path = "D:/推广/"+brand+"/日报/日报"
    zipfile_list = os.listdir(original_file_path)

# %%
    for _file in zipfile_list:
        if _file.endswith(".zip"):
            file_need_zip = _file
            pu.extract_zipfile(original_file_path+"/"+file_need_zip,zipped_file_path)
            temp_csv_file = os.listdir(zipped_file_path)[0]
            excel_file_name = re.search("[a-zA-Z\\u4e00-\\u9fa5]+",file_need_zip).group()
            print(excel_file_name)
            pu.csv_to_excel(zipped_file_path+"/"+temp_csv_file,cleaned_file_path+"/"+"/日报数据源/"+excel_file_name+".xlsx",name_of_sheet=excel_file_name)
            pu.clear_folder(zipped_file_path)
        else:
            continue

# %%
#JZT处理#
alinamin_JZT_path = "D:/推广/alinamin/日报"
pu.csv_to_excel(alinamin_JZT_path+"/JZT.csv",alinamin_JZT_path+"/JZT.xlsx",name_of_sheet="JZT")

# %%
#pu.refresh_and_save_excel("D:/推广/alinamin/日报/Alinamin推广日报底表.xlsx",excel_output_path+"/"+brand+"推广日报"+datetime.strftime(datetime.today()-timedelta(days=1),"%m%d")+".xlsx")



