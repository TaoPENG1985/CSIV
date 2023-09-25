import os

def get_filename(path,filetype):  # 输入路径、文件类型例如'.csv'
    name = []
    for root,dirs,files in os.walk(path):
        for i in files:
            if os.path.splitext(i)[1]==filetype:
                name.append(i)    
    return name
