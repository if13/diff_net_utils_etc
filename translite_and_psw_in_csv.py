import pandas as pd

import pytils.translit as trans
import random
import pprint
import string

FILE = 'out_ld.csv' 

df = pd.read_csv(FILE)
print(df.head())

#k - длинна пароля
def gen_passw(k=8): 
    passw = ''.join(random.sample('123456789qwertyuipasdfghjkzxc'
                                          'vbnmQWERTYUPASDFGHJKLZXCVBNM', k))
    #print(passw, 'before if')
    if (set(passw)&set(string.ascii_uppercase) and
        set(passw)&set(string.digits) and
        set(passw)&set(string.ascii_lowercase)):
           return passw
    else:
        return gen_passw()


def translit(full_name):
    user_rus = [i.strip() for i in full_name.strip().split()]
    user_en = [trans.translify(n).lower().replace("'", "") for n in user_rus]
    user_en = '{}-{:.1}{:.1}'.format(*user_en)
    return user_en
    
# заполняем логины и пароли
#df['sAMAccountName'] = df['FullName'].apply(lambda x: translit(x))
#df['Password'] = df['Password'].apply(lambda x: gen_passw())

#df.to_csv('out.csv', index=False)  

# формируем файл на печать

df = df.drop(columns=['Path', 'Groups'])
df.rename(columns={"FullName": "ФИО пользователя",
                   "sAMAccountName": "Имя пользователя(login)"}, inplace=True)

with open('output.html', 'w') as f:
    # Итерация по строкам DataFrame
    page_num=1
    count = 0
    
    for index, row in df.iterrows():
        f.write('<hr />')
        f.write('<p>\n')  # Начинаем новый абзац для каждой строки
        f.write('<p><span><strong>КАРТОЧКА ДОСТУПА К СЕТИ</strong></span></p>')
        # Итерация по столбцам DataFrame
        for column, value in row.items():
            f.write(f'<b>{column}:</b> {value}<br>\n')  # Печать имени столбца и его значения
        
        f.write('<p><strong>Информация, содержащаяся в карточке, является конфиденциальной!!!</strong></p>')
        f.write('</p>\n')  # Закрываем абзац для строки
        
        count += 1
        if count >= 6:
                f.write('<div style="page-break-before: always;"></div>')
                count=0
        
        
print("Данные успешно выведены в файл output.html")



