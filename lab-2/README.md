Лабораторна робота No2
Наука про дані: підготовчий етап
ФБ-25 Маслюк Влад

import urllib.request
import pandas as pd
import requests
import os
import glob
from datetime import datetime

directory = 'csv_lab2'
files = os.listdir(directory)

def download_file(ids):
    date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    vhi_url = urllib.request.urlopen(url)
    file_name = f'{directory}/NOAA_ID_{ids}_{date_now}.csv'
    out = open(file_name, 'wb')
    out.write(vhi_url.read())
    out.close()
    print(f"data id {ids} downloaded")

def file_exists(directory, id):
    files = os.listdir(directory)
    for file in files:
        if file.startswith(f"NOAA_ID_{id}_") and file.endswith(".csv"):
            return True
    return False
    
if(not os.path.exists(directory)):
        os.makedirs(directory)
else:
        print("Dir is already exists.")  
    
for ids in range(1, 28):
    url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={ids}&year1=1981&year2=2024&type=Mean"
    response = requests.get(url)
    if response.status_code == 200:
        files_to_delete = glob.glob(f"{directory}/NOAA_ID_{ids}_*.csv")
        if files_to_delete is not None:
            for file_to_delete in files_to_delete:
                    os.remove(file_to_delete)
        if file_exists(directory, ids) == False:
            print(f"data exists {ids}")
            download_file(ids)
    else:
        print(f"Download complete")
        break
print(f"Download complete")

![image](https://github.com/purplefish1412/ad_labs/assets/144566930/346c5334-042d-4fab-8750-4c3cc7fb44c8)



files = os.listdir(directory)
df_all = pd.DataFrame()

for file in files:
    headers = ['Year', 'Week', ' SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    df = pd.read_csv(f'{directory}/{file}', header=1, names=headers, skiprows=1)[:-1]
    df = df.drop(df.loc[df['VHI'] == -1].index)
    if file.split('_')[2].isdigit():
        df['area'] = int(file.split('_')[2])
        df = df.drop(columns=['empty'])
        df_all = df_all.dropna(axis=1, how='all')
        df_all = pd.concat([df_all, df], ignore_index=True)
    else:
        None

print(df_all, "\n")

![image](https://github.com/purplefish1412/ad_labs/assets/144566930/3f3f5bf0-eeb7-4084-ab9b-bb595d6ba866)

indexes = ["22", "24", "23", "25", "3", "4", "8", "19", "20", "21", "9", "26", "10", "11",
                            "12", "13", "14", "15", "16", "27", "17", "18", "6", "1", "2", "7", "5"] 
dict = {i+1: indexes[i] for i in range(len(indexes))} 
df_all.area.replace(dict, inplace=True)  
df_all.to_csv(f"{directory}/NOAA_ALL_CSV.csv")  
print(df_all)
df_all['Year'] = df_all["Year"].astype(int)
df_all['area'] = df_all["area"].astype(int)

![image](https://github.com/purplefish1412/ad_labs/assets/144566930/ac836881-a823-43de-96f9-18878f44253f)

![image](https://github.com/purplefish1412/ad_labs/assets/144566930/267769fd-dd06-4196-a9b8-b465baac81eb)


def find_vhi(area, year):
    df_search = df_all[(df_all.area == area) & (df_all.Year == year)][['Week', 'VHI']]
    print(f"VHI  {area} in {year}")  
    print(df_search)  
    print("...")
    
def find_extremums(area, year):
    max_v = df_all[(df_all.Year.astype(int) == int(year)) & (df_all.area == area)]['VHI'].max()  
    min_v = df_all[(df_all.Year.astype(int) == int(year)) & (df_all.area == area)]['VHI'].min()  
    print(f'max: {max_v}')  
    print(f'min: {min_v}\n')  
    return

find_vhi(6, 2001)
find_extremums(6, 2001)

    ![image](https://github.com/purplefish1412/ad_labs/assets/144566930/7ff5fa16-2122-4f89-8561-cfa592ad0e15)
    ![image](https://github.com/purplefish1412/ad_labs/assets/144566930/9d7f240d-e444-4449-b405-4fa88b98f06b)

def vhi_range(areas, min_year, max_year):
    if not isinstance(areas, list) or not areas:
        return print('No data')
    df_all['Year'] = df_all['Year'].astype(int)
    result = df_all[(df_all['Year'] >= min_year) & (df_all['Year'] <= max_year) & (df_all['area'].isin(areas))][['Year', 'VHI', 'area']]
    if result.empty:
        print('No matching data')
    return result

result = vhi_range([4, 5], 1995, 2002)
print(result)

![image](https://github.com/purplefish1412/ad_labs/assets/144566930/c8b2ee91-d88a-4af9-8175-c2f0ecd177ec)


def extreme_droughts(prc):
    df_all['Year'] = df_all['Year'].astype(int)
    
    df_drought = df_all[(df_all['VHI'] <= 15) & (df_all['VHI'] != -1)]
    group = df_drought.groupby('Year')['area'].nunique()
    res = group[group > ((25 * prc) / 100)].reset_index()
    return res

print(extreme_droughts(20))

![image](https://github.com/purplefish1412/ad_labs/assets/144566930/f1854fd5-83eb-4910-995e-765bc4bad8a1)


def mid_droughts(prc, vhi_min=15, vhi_max=40):
    df_all['Year'] = df_all['Year'].astype(int)
    
    df_drought = df_all[(df_all['VHI'] >= vhi_min) & (df_all['VHI'] <= vhi_max)]
    group = df_drought.groupby('Year')['area'].nunique()
    areas = df_all['area'].nunique()
    res = group[group > ((areas * prc) / 100)].reset_index()
    return res

print(mid_droughts(20))

![image](https://github.com/purplefish1412/ad_labs/assets/144566930/ad98d612-e219-4d67-851a-c6257a37f877)

