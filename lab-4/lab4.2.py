import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

file_name = "data/adult.data"
headers = ['Age', 'Work_class', 'Final_weight', 'Education', 'Education_num', 'Marital_status', 'Occupation', 'Relationship', 'Race', 'Sex', 'Capital_gain', 'Capital_loss',
           'Hours_per_week', 'Native_country', 'Income']

def readfile(file, header):
    df_fun = pd.read_csv(file, sep=",", header=1, names=header, na_values='?')
    return df_fun

df = readfile(file_name, headers)
print(df)

def readfile_np(file, header):
    array = np.genfromtxt(file, delimiter=', ', dtype=None, names=header, encoding=None, skip_header=1)
    return array

data_array = readfile_np(file_name, headers)
print(data_array)

df = df.dropna()
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
df = df[~df.isin(['?']).any(axis=1)]

if df.isna().any().any() or (df == '?').any().any():
    print("пусті зачення присутні")
else:
    print("немає пустих значень")

print(df)

string_data_array = np.array([tuple(str(item) for item in row) for row in data_array])
mask = np.all((string_data_array != '?') & (string_data_array != 'nan'), axis=1)
cleaned_data_array = string_data_array[mask]
has_question_mark = np.any(cleaned_data_array == '?')
if has_question_mark:
    print("пусті зачення присутні")
else:
    print("немає пустих значень")
    
#Завдання 2
    
def normalize(column):
    return (column - column.min()) / (column.max() - column.min())

columns_to_normalize = ['Hours_per_week', 'Age', 'Final_weight', 'Capital_gain', 'Capital_loss']

df_normalize = df.copy()
for col in columns_to_normalize:
    df_normalize[col] = normalize(df[col])

print(df_normalize)


dtype = [('Age', '<U6'), ('Work_class', '<U16'), ('Final_weight', '<U6'), ('Education', '<U12'), ('Education_num', '<U6'), ('Marital_status', '<U21'), ('Occupation', '<U17'), ('Relationship', '<U14'), ('Race', '<U18'), ('Sex', '<U6'), ('Capital_gain', '<U6'), ('Capital_loss', '<U6'), ('Hours_per_week', '<U6'), ('Native_country', '<U26'), ('Income', '<U5')]

structured_array = np.array([tuple(row) for row in cleaned_data_array], dtype=dtype)

data_array_normalize = structured_array.copy()

for col in columns_to_normalize:
    data_array_normalize[col] = normalize(data_array_normalize[col].astype(float))

print(data_array_normalize)

#Завдання 3

min_value_hours = df_normalize['Education_num'].min()
max_value_hours = df_normalize['Education_num'].max()

plt.figure(figsize=(10, 7))
sns.histplot(df_normalize['Education_num'], bins=10, binrange=(min_value_hours, max_value_hours))

plt.xlabel('Номер навчального року (по кількості навчання)')
plt.ylabel('Кількість входжень')
plt.title('Показ кількості входжень в діапазони навчальних років')
plt.show()


min_value_hours = data_array_normalize['Education_num'].astype(float).min()
max_value_hours = data_array_normalize['Education_num'].astype(float).max()

plt.figure(figsize=(10, 7))
sns.histplot(data_array_normalize['Education_num'].astype(float), bins=10, binrange=(min_value_hours, max_value_hours))

plt.xlabel('Номер навчального року (по кількості навчання)')
plt.ylabel('Кількість входжень')
plt.title('Показ кількості входжень в діапазони навчальних років')
plt.show()

#Завдання 4

plt.figure(figsize=(10, 7))
sns.scatterplot(data=df_normalize, x='Final_weight', y='Age')

plt.xlabel('Кінцева вага')
plt.ylabel('Вік')
plt.title('Графік залежності навчання до віку')
plt.show()

plt.figure(figsize=(10, 7))
sns.scatterplot(x=data_array_normalize['Final_weight'].astype(float), y=data_array_normalize['Age'].astype(float))

plt.xlabel('Кінцева вага')
plt.ylabel('Вік')
plt.title('Графік залежності навчання до віку')
plt.show()

#Завдання 5 

def pearson_coef(df):
    pearson_coef = df['Age'].corr(df['Final_weight'], method='pearson')
    return round(pearson_coef, 3)

def spearman_coef(df):
    spearman_coef = df['Final_weight'].corr(df['Age'], method='spearman')
    return round(spearman_coef, 3)

print(f'Коефіцієнт Спірсона: {spearman_coef(df_normalize)}')
print(f'Коефіцієнт Пірсона: {pearson_coef(df_normalize)}')

def pearson_coef_np(array):
    pearson_coef = np.corrcoef(array['Age'].astype(float), array['Final_weight'].astype(float))[0, 1]
    return round(pearson_coef, 3)

def spearman_coef_np(array):
    data1_rank = np.argsort(np.argsort(array['Age'].astype(float)))
    data2_rank = np.argsort(np.argsort(array['Final_weight'].astype(float)))
    
    d = data1_rank - data2_rank
    d_squared = d**2
    
    sum_d_squared = np.sum(d_squared)
    
    n = len(array)
    spearman_coef = 1 - (6 * sum_d_squared) / (n * (n**2 - 1))
    return round(spearman_coef, 3)

print(f'Коефіцієнт Спірсона: {spearman_coef_np(data_array_normalize)}')
print(f'Коефіцієнт Пірсона: {pearson_coef_np(data_array_normalize)}')

#Завдання 6

one_hot = pd.get_dummies(df_normalize['Race'])
df_encode = df_normalize.join(one_hot)
for column in one_hot.columns:
    df_encode[column] = df_encode[column].astype(int)

print(df_encode)

column = data_array_normalize['Race']
unique_value = np.unique(column)
value_to_index = {value: index for index, value in enumerate(unique_value)}
indexed_column = np.vectorize(value_to_index.get)(column)
one_hot_encoded_column = np.eye(len(unique_value))[indexed_column]
one_hot_encoded_data = cleaned_data_array.copy()
one_hot_encoded_data = np.hstack((one_hot_encoded_data, one_hot_encoded_column))

print(one_hot_encoded_data)

#Завдання 7

rs = round(df_normalize[headers].describe(),2)
print(rs)

cols = ['Age', 'Final_weight', 'Education_num', 'Capital_gain', 'Capital_loss', 'Hours_per_week']
pp = sns.pairplot(df_normalize[cols], height=1.8, aspect=1.8,
                  plot_kws=dict(edgecolor="k", linewidth=0.5),
                  diag_kind="kde", diag_kws=dict(fill=True))

fig = pp.fig 
fig.subplots_adjust(top=0.93, wspace=0.3)
t = fig.suptitle('Попарні графіки атрибутів дорослих', fontsize=14)
plt.show()

