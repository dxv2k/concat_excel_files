import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from tqdm import tqdm # progress bar  
from datetime import datetime
import pandas as pd
import numpy as np 
import os 

COLOR_YELLOW = '\033[33m'
COLOR_GREEN = '\033[32m'

DATA_PATH = "./data/"
CURR_YEAR = datetime.now().year
FILE_LIST = os.listdir(DATA_PATH)

# columns used in merged file
columns =  ["Mã BN","Họ và tên BN", "Năm sinh", "Giới Tính","Tuổi","Địa Chỉ"]

# create empty dataframe with columns name
dataframe = pd.DataFrame(columns=[str(i) for i in columns])

total_patients = 0
# copy from files to dataframe & add new columns   
for file in tqdm(FILE_LIST, total=len(FILE_LIST)): 
    curr_data = pd.read_excel(DATA_PATH + file)
    total_patients += len(curr_data)

    # get columns 1,2,3,4 (idx start at 0) 
    # mã BN, họ tên BN, năm sinh, giới tính 
    address_data = curr_data.iloc[:,5:9]
    curr_data = curr_data.iloc[:,1:5]

    # remove headers 
    curr_data = curr_data[:].values

    # add column age & append to list 
    age_list = []
    for row in curr_data: 
        try: 
            age_list.append(CURR_YEAR - int(row[2]))
        except ValueError: 
            age_list.append(0)
    # convert & reshape to numpy vector 
    age_list = np.asarray(age_list)
    age_list = age_list.reshape((age_list.shape[0],1)) 

    # add column address & append to list 
    address_list = address_data.values.tolist() 
    for idx,address in enumerate(address_list): 
        address_list[idx] = ' '.join([val for val in address_list[idx] if isinstance(val,str)])
    address_list = np.asarray(address_list)
    address_list = address_list.reshape((address_list.shape[0],1)) 

    # concate dataframe & age_list & address_list 
    curr_data = np.hstack((curr_data,age_list,address_list))

    # convert & append to dataframe 
    curr_data = pd.DataFrame(curr_data, columns=columns)
    dataframe = dataframe.append(curr_data, ignore_index=True)

# Check if matching 
print("="*20)
print(COLOR_YELLOW + "Accumulate patients in all files: ",total_patients)
print(COLOR_YELLOW + "Total in output: ",len(dataframe))
print("="*20)

print(COLOR_GREEN + "Saving result to file...")
dataframe.to_excel("./output.xlsx",sheet_name="Tổng hợp")

# keep command line open  
input("Press any key to exit...")