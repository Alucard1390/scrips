import promutil as pu

#每天登陆时重置源数据文件夹(清空文件夹)

brands_list = ["雪肌精","盐野义","GA","alinamin"]

folder_list = []
for brand in brands_list:
    folder_list.append("D:/推广/"+brand+"/日报/每日数据源")
    folder_list.append("D:/推广/"+brand+"/日报/日报数据源")

for folder_route in folder_list:
    pu.clear_folder(folder_path=folder_route)