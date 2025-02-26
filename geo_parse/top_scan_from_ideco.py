import re
import geoip2.database
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt 


# Открываем базы данных GeoLite2
reader_country = geoip2.database.Reader("GeoLite2-Country.mmdb")
reader_city = geoip2.database.Reader("GeoLite2-City.mmdb")
# Парсит данные из csv из 
# Загрузка данных
df = pd.read_csv('system_logs.csv')

# Функция для получения страны
def get_country(ip):
    try:
        return reader_country.country(ip).country.name
    except:
        return "Unknown"

# Функция для получения города
def get_city(ip):
    try:
        return reader_city.city(ip).city.name
    except:
        return "Unknown"

# Функция для парсинга строки лога
def add_col_df(log):
    pattern = r"src (\S+).*?dport (\d+)"
    match = re.search(pattern, log)
    if match:
        src, dport = match.groups()
        return pd.Series({
            "src": src,
            "src_country": get_country(src),
            "src_city": get_city(src),
            "dport": dport
        })
    return pd.Series({"src": None, "src_country": None, "src_city": None, "dport": None})

# Применяем функцию к колонке message
df_new = df.join(df["message"].apply(add_col_df))

# Закрываем базы данных
reader_country.close()
reader_city.close()

# Сохраняем результат
df_new.to_csv("parsed_logs.csv", index=False)


df_top_cntr = df_new['src_country'].value_counts()[:10].reset_index()
df_top_cntr.columns = ['Country', 'Count']  # Переименовываем столбцы
#plt.pie(data=df_top_cntr, labels='Country', x = 'Count',autopct='%.0f%%')
#plt.show()


df_top_ports = df_new['dport'].value_counts().reset_index()[:10]

df_top_ports.columns = ['dport', 'Count']  # Переименовываем столбцы
plt.pie(data=df_top_ports, labels='dport', x = 'Count',autopct='%.0f%%')




