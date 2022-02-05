import pandas as pd
import os 

DATA_PATH = "./data/"

file_list = os.listdir(DATA_PATH)

# columns used in merged file
columns =  ["Mã BN","Họ và tên BN", "Năm sinh", "Giới Tính"]

# create empty dataframe with columns name
df = pd.DataFrame(columns=[str(i) for i in columns])

# copy from files to dataframe 
for idx, file in enumerate(file_list): 
    curr_data = pd.read_excel(DATA_PATH + file)

    # get columns 1,2,3,4 (idx start at 0) 
    # mã BN, họ tên BN, năm sinh, giới tính 
    curr_data = curr_data.iloc[:,1:5]

    # remove headers 
    curr_data = curr_data[:].values

    # convert to dataframe 
    curr_data = pd.DataFrame(curr_data, columns=columns)

    df = df.append(curr_data, ignore_index=True)

df.to_excel("./output.xlsx",sheet_name="Tổng hợp")