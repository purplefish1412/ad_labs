import numpy as np
import pandas as pd
import timeit
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def avg_time(func, num_iterations=10):
    time_taken = timeit.timeit(stmt=func, globals=globals(), number=num_iterations)
    average_time = time_taken / num_iterations
    return average_time

list_time_pd = []
list_time_np = []

file_name = r'household_power_consumption.txt'
with open(file_name, 'r') as file:
    first_line = file.readline()
headers = first_line.rstrip('\n').split(";")
print(headers)

def readfile(file, header):
    df_fun = pd.read_csv(file, sep=";", header=1, names=header, na_values=['?'])
    return df_fun

pd_time = avg_time('readfile(file_name, headers)')
list_time_pd.append(pd_time)
print(f'Сер час Pandas для зчитування файлу: {pd_time}')

df = readfile(file_name, headers)
print(df)

def readfile_np(file, header):
    array = np.genfromtxt(file, delimiter=';', dtype=None, names=header, encoding=None, skip_header=1)
    return array

np_time = avg_time('readfile_np(file_name, headers)')
list_time_np.append(np_time)        
print(f'Сер час Numpy для зчитування файлу: {np_time}')

data_array = readfile_np(file_name, headers)
print(data_array)

df = df.dropna()

if df.isna().any().any() or (df == '?').any().any():
    print("пусті зачення присутні")
else:
    print("немає пустих значень")
    
string_data_array = np.array([tuple(str(item) for item in row) for row in data_array])
mask = np.all((string_data_array != '?') & (string_data_array != 'nan'), axis=1)
cleaned_data_array = string_data_array[mask]
if np.any(cleaned_data_array == '?'):
    print("пусті зачення присутні")
else:
    print("немає пустих значень")
    
dtype = [('Date', '<U10'), ('Time', '<U8'), ('Global_active_power', '<U6'), ('Global_reactive_power', '<U5'), ('Voltage', '<U7'), ('Global_intensity', '<U6'), ('Sub_metering_1', '<U6'), ('Sub_metering_2', '<U6'), ('Sub_metering_3', '<f8')]

structured_array = np.array([tuple(row) for row in cleaned_data_array], dtype=dtype)

def select_households(df):
    return df[df['Global_active_power'] > 5]

pd_time = avg_time('select_households(df)')
list_time_pd.append(pd_time)
print(f'Сер час Pandas для вибірки: {pd_time}')

df_households = select_households(df) 
print(df_households)

def select_households_np(array):
    mask = array['Global_active_power'].astype(float) > 5
    selected_rows = array[mask]
    return selected_rows

np_time = avg_time('select_households_np(structured_array)')
list_time_np.append(np_time)        
print(f'Сер час Numpy для вибірки: {np_time}')

array_households = select_households_np(structured_array)
print(array_households)

print("Завдання 2")

def households_volt(df):
    return df[df['Voltage'] > 235]

pd_time = avg_time('households_volt(df)')
list_time_pd.append(pd_time)
print(f'Сер час Pandas для вибірки: {pd_time}')

df_households = households_volt(df) 
print(df_households)

def households_volt_np(array):
    mask = array['Voltage'].astype(float) > 235
    selected_rows = array[mask]
    return selected_rows

np_time = avg_time('households_volt_np(structured_array)')
list_time_np.append(np_time)        
print(f'Серчас Numpy для вибірки: {np_time}')

array_households = households_volt_np(structured_array)
print(array_households)

print("Завдання 3")

def households_appliances(df):
    df = df[df['Global_intensity'].between(19, 20)]
    return df[df['Sub_metering_2'] > df['Sub_metering_3']]

pd_time = avg_time('households_appliances(df)')
list_time_pd.append(pd_time)
print(f'Сер час Pandas для вибірки: {pd_time}')

df_intensity = households_appliances(df)
print(df_intensity)

def households_appliances_np(array):
    mask = (array['Global_intensity'].astype(float) >= 19.0) & (array['Global_intensity'].astype(float) <= 20.0) & ((array['Sub_metering_2'].astype(float)) > array['Sub_metering_3'].astype(float))
    selected_rows = array[mask]
    return selected_rows

np_time = avg_time('households_appliances_np(structured_array)')
list_time_np.append(np_time)        
print(f'Сер час Numpy для вибірки: {np_time}')

array_households = households_appliances_np(structured_array)
print(array_households)

print("Завдання 4")

def households_random(df):
    random_household = df.sample(n=500000, replace=False).sort_index()
    return random_household

pd_time = avg_time('households_random(df)')
list_time_pd.append(pd_time)
print(f'Сер час Pandas для випадкової вибірки: {pd_time}')

random_household = households_random(df)
print(random_household)

def households_random_np(array):
    num_rows = array.shape[0]
    random_indices = np.random.choice(num_rows, size=500000, replace=False)
    random_rows = array[random_indices]
    return random_rows

np_time = avg_time('households_random_np(structured_array)')
list_time_np.append(np_time)        
print(f'Сер час Pandas для випадкової вибірки: {np_time}')

random_array = households_random_np(structured_array)
print(random_array)

print("Завдання 5")

def after_18(df):
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')
    after_18_df = df[df['Time'].dt.time > pd.to_datetime('18:00:00', format='%H:%M:%S').time()].copy()
    after_18_df['Time'] = after_18_df['Time'].dt.strftime('%H:%M:%S')
    after_18_df = after_18_df[after_18_df['Global_active_power'] > 6]
    return after_18_df

pd_time = avg_time('after_18(random_household)')
list_time_pd.append(pd_time)
print(f'Сер час Pandas для вибірки: {pd_time}')

after_18_df = after_18(random_household)
print(after_18_df)

def choose_group_2(df):
    after_18_df_group_2 = df[(df['Sub_metering_2'] > df['Sub_metering_1']) & (df['Sub_metering_2'] > df['Sub_metering_3'])]
    return after_18_df_group_2

pd_time = avg_time('choose_group_2(after_18_df)')
list_time_pd.append(pd_time)
print(f'Сер час Pandas для вибірки за групами: {pd_time}')

after_18_df_group_2 = choose_group_2(after_18_df)
print(after_18_df_group_2)


def half_results(df):
    filtered_first_half = df.iloc[:len(df) // 2:3]
    filtered_second_half = df.iloc[len(df) // 2::4]
    return filtered_first_half, filtered_second_half

pd_time = avg_time('half_results(after_18_df_group_2)')
list_time_pd.append(pd_time)
print(f'Сер час Pandas для розділення датафрейму: {pd_time}')

filtered_first_half, filtered_second_half = half_results(after_18_df_group_2)
final_df = pd.concat([filtered_first_half, filtered_second_half])
print(final_df)

def after_18_np(array):
    time_data = np.array([datetime.strptime(t, "%H:%M:%S") for t in array['Time']])
    time = datetime.strptime("18:00:00", "%H:%M:%S")
    selected_rows_after_18 = array[time_data >= time]
    selected_rows_after_18 = selected_rows_after_18[selected_rows_after_18['Global_active_power'].astype(float) > 6]
    return selected_rows_after_18

np_time = avg_time('after_18_np(random_array)')
list_time_np.append(np_time)        
print(f'Сер час Numpy для вибірки: {np_time}')

selected_households_after_18 = after_18_np(random_array)
print(selected_households_after_18)


def choose_group_2_np(array):
    array = array[(array['Sub_metering_2'].astype(float) > array['Sub_metering_1'].astype(float)) & (array['Sub_metering_2'].astype(float) > array['Sub_metering_3'].astype(float))]
    return array

np_time = avg_time('choose_group_2_np(selected_households_after_18)')
list_time_np.append(np_time)        
print(f'Сер час Numpy для вибірки за групами: {np_time}')

selected_households_group_2 = choose_group_2_np(selected_households_after_18)
print(selected_households_group_2)


def half_results_np(array):
    first_half, second_half = np.array_split(array, 2)
    selected_first_half = first_half[::3]
    selected_second_half = second_half[::4]
    return selected_first_half, selected_second_half

np_time = avg_time('half_results_np(selected_households_group_2)')
list_time_np.append(np_time)        
print(f'Сер час Numpy для розділення датафрейму: {np_time}')

selected_first_half, selected_second_half = half_results_np(selected_households_group_2)
print(selected_first_half, '\n')
print(selected_second_half)


operations = ['Зчитання файлу', 'домогосподарства > 5 кВт', 'домогосподарства > 235 В', 'домогосподарства 19-20 А', 'Обрати випадковим чином 500000 домогосподарств', 'домогосподарства після 18:00 > 6 кВт', 'група 2', 'Вибірка елементів']

plt.figure(figsize=(20, 8))

sns.lineplot(x=operations, y=list_time_pd, marker='o', label='pandas')
sns.lineplot(x=operations, y=list_time_np, marker='o', label='numpy')
plt.xlabel('Оцерації')
plt.ylabel('cек')
plt.title('Час')
plt.legend()
plt.xticks(rotation=15)
plt.show()