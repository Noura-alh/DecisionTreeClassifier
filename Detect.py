from DT import DecisionTree
from DBconnection import connection2
import pandas as pd
from DBconnection import connection1, SMI_engine
from GeneralSearch import GeneralSearch




cur1, db1, engine1 = connection1() #SMI_DB

cur2, db2, engine2 = connection2() #bank_DB


'''df = pd.read_csv('GeneratedDataset.csv')
df.to_sql(name='transaction', con=engine2, if_exists='append',
                              index=False)'''

#classifier = DecisionTree()
#classifier.DecisionTreeClassifier()


#MULTI CERTIREA

#Create profiles
cur2.execute('SELECT clientID, clientName FROM bank_db.transaction')
result = list(set(list(cur2.fetchall())))

#get client how flagged suspious transactions
cur1.execute('SELECT clientName FROM SMI_DB.SuspiciousTransaction')
suspsuoiusClient = list(set(list(cur1.fetchall())))
print(suspsuoiusClient)


i = 1
for id, name in result:
    query = "INSERT INTO Client (clientID, clientName) VALUES(%s,%s)"
    val = (id, name)
    #print(name)
    cur1.execute(query, val)
    dt_class = 0
    mc_class = 0
    transaction_class =0
    profile_class = 0
    GeneralSearch_result=0
    GeneralSearch_class =0

    flag = False
    # If the client has any suspsuoius transaction run general search
    if any(name in s for s in suspsuoiusClient):
        dt_class = 1
        search = GeneralSearch('"' + name + '"', id)
        search.twitter_search()
        GeneralSearch_result, GeneralSearch_class = search.google_search()


    #mc_class = multiCertire.score
    profile_class = (0.5 * dt_class) + (0.5 * mc_class)
    if 0.7 < profile_class <= 1:
        profile_class = 'High'
    elif 0.33 < profile_class <= 0.7:
        profile_class = 'Medium'
    elif 0 < profile_class <= 0.33:
        profile_class = 'Low'
    else:
        profile_class = 'Clean'

    try:
        transaction_class = ((dt_class + mc_class) / 2)
    except ZeroDivisionError:
        transaction_class = 0

    print('client Name: ', name)
    print('search_result: ', GeneralSearch_result)
    print('transaction_class: ', transaction_class)
    print('GeneralSearch_class: ', GeneralSearch_class)
    print('profile class: ', profile_class)


    cur1.execute("UPDATE SMI_DB.Client SET profileClassification= '%s'WHERE clientID='%s' " % (profile_class, id))






















'''for clientName in suspTransction AND multiCertire.dropDuplication  :

    ### genrate profile without profile_class or general_searchResult ####
    general_search_class = generalSearch(clientName)
    if clientName in suspTransction:
        dt_class = 1
    if clientName in multiCertire:
        mc_class = multiCertire.score
    profile_class = (0.5*dt_class) + (0.5*mc_class)

    ### INSERT  prodile_class  ####

    if 0.7 < profile_class <= 1:
        clientClass = 'High'
    elif 0.33 < profile_class <= 0.7:
        clientClass = 'Medium'
    elif 0 < profile_class <= 0.33:
        clientClass = 'Low'
    else:
        clientClass = 'Clean'  '''

    ## case



'''
cur, db, engine = connection2()
df_suspiciousTransactions = pd.read_csv('testingRecordes.csv')
df_suspiciousTransactions.to_sql(name='transactions', con=engine, if_exists ='append', index=False) #appened work

'''

'''dt_class = 0
mc_class = 0
profile_class = 0
search = GeneralSearch('"حجاج العجمي"', 1966002811)
search.twitter_search()
GeneralSearch_result, GeneralSearch_class = search.google_search()
print('client Name: ', '"حجاج العجمي"')
print('search_result: ', GeneralSearch_result)
print('client_class: ', GeneralSearch_class)'''
