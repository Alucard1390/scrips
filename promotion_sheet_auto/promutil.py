import os
import pandas as pd
import zipfile
import re
import shutil
import win32com.client as win32
from datetime import datetime,timedelta


def extract_zipfile(zipfile_path, target_folder):
    with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
        zip_ref.extractall(target_folder)

def csv_to_excel(csvfile_path,excelfile_path,name_of_sheet):
    try:
        df = pd.read_csv(csvfile_path,encoding="GBK")
    except:
        df = pd.read_csv(csvfile_path,encoding="UTF-8")
    df.to_excel(excelfile_path,index=False,sheet_name=name_of_sheet)

def clear_folder(folder_path):
    """清空文件夹（删除后重建）"""
    try:
        # 删除整个文件夹
        shutil.rmtree(folder_path)
        # 重新创建空文件夹
        os.makedirs(folder_path, exist_ok=True)
    except Exception as e:
        print(f"清空文件夹失败: {e}")

def refresh_and_save_excel(input_path, output_path):
    """
    打开 Excel 文件，刷新所有数据（公式、透视表等），并另存为新文件
    需要已安装 Microsoft Excel 应用程序
    
    参数:
        input_path (str): 输入 Excel 文件路径
        output_path (str): 输出 Excel 文件路径
    """
    try:
        # 启动 Excel 应用程序
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.Visible = False  # 后台运行
        excel.DisplayAlerts = False # 强制覆盖不弹窗
        
        # 打开工作簿
        wb = excel.Workbooks.Open(os.path.abspath(input_path))
        
        # 刷新所有数据
        wb.RefreshAll()  # 刷新公式、透视表、数据连接等
        excel.CalculateUntilAsyncQueriesDone()  # 等待刷新完成
        
        # 另存为新文件（不覆盖原文件）
        wb.Save()
        wb.SaveAs(os.path.abspath(output_path))
        print(f"已刷新并另存为: {output_path}")
        
    except Exception as e:
        print(f"操作失败: {e}")
    finally:
        # 关闭工作簿和 Excel
        wb.Close(SaveChanges=True)
        excel.Quit()
        # 释放 COM 对象
        del excel

brand_info_list = []
brand_info_sekkisei = {}
brand_info_sekkisei["brand"] = "雪肌精"
brand_info_sekkisei["account"] = "雪肌精官方旗舰店:李焕"
brand_info_sekkisei["pwd"] = "LH17368904761"

brand_info_alinamin = {}
brand_info_alinamin["brand"] = "alinamin"
brand_info_alinamin["account"] = "alinamin爱利纳明海外旗舰:李焕"
brand_info_alinamin["pwd"] = "alinamin123"

brand_info_list.append(brand_info_sekkisei)
brand_info_list.append(brand_info_alinamin)