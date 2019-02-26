import pandas as pd
import mysql.connector
from sqlalchemy import create_engine


'''engine = create_engine("mysql+mysqlconnector://root:SMIhmwn19*@localhost/Bank_DB")

df = pd.read_csv('GeneratedDataset.csv')
df.to_sql(name='transaction', con=engine, if_exists='append',
                              index=False)

db = mysql.connector.connect(host="localhost",
                             user="root",
                             passwd="SMIhmwn19*",
                             db="Bank_DB",
                             autocommit=True)
cur2 = db.cursor()

cur2.execute('SELECT clientID, clientName FROM Bank_DB.transaction')
result = list(set(list(cur2.fetchall())))'''


from datetime import datetime, timedelta, time
db = mysql.connector.connect(host="localhost",
                             user="root",
                             passwd="SMIhmwn19*",
                             db="SMI_DB",
                             autocommit=True)
cur2 = db.cursor()

clientID = 305934
SearchClass = 0.7
date_now = datetime.now()
formatted_date = date_now.strftime('%Y-%m-%d %H:%M:%S')


#cur2.execute("UPDATE SMI_DB.Client SET generalSearchDate=%s, generalSearchResult=%s  WHERE clientID=%s " % (formatted_date, SearchClass, clientID))
cur2.execute("UPDATE SMI_DB.Client SET generalSearchDate= '%s', generalSearchResult= '%s' WHERE clientID='%s' " % (formatted_date,SearchClass, clientID ))






'''
cur2.execute('SELECT searchDate FROM SMI_DB.generalSearch WHERE searchID = 210')
date_past = cur2.fetchone()
print(date_past)

date_now = datetime.now()
formatted_date = date_now.strftime('%Y-%m-%d')
#formatted_date2 = date_past.strftime('%Y-%m-%d')

from dateutil.parser import parse

#date_past = parse(formatted_date2)
date_now = parse(formatted_date)

print(date_now - date_past)'''


'''past < present
True
datetime(3000, 1, 1) < present
False
 present - datetime(2000, 4, 4)
datetime.timedelta(4242, 75703, 762105)'''

