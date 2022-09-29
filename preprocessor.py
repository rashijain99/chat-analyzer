import pandas as pd
import re

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[a-zA-Z][a-zA-Z]\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_msg':messages , 'msg_dates':dates})
    df['msg_dates'] = pd.to_datetime(df['msg_dates'], format = '%d/%m/%y, %H:%M %p - ')
    df.rename(columns= {'msg_dates':'date'}, inplace = True)

    users = []
    messages = []
    for msg in df['user_msg']:
        entry = re.split('([\w\W]+?):\s',msg)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notifications')
            messages.append(entry[0])
            
    df['user'] = users       
    df['message'] = messages

    df.drop(columns= ['user_msg'],inplace =True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['only_date'] = df['date'].dt.date
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['day_name'] = df['date'].dt.day_name()
    df['month_name'] = df['date'].dt.month_name()

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df