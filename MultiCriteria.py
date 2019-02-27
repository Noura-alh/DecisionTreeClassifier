import pandas
from DBconnection import connection2
import mysql.connector


class MultiCriteria:
    def __init__(self):

        cur, db, engine = connection2()


        self.ADestID = []
        self.ADestname = []
        self.Alocation = []
        self.Aamount = []
        self.Aavg = []


        cur.execute('SELECT clientID FROM bank_db.transaction')
        record = list(set(list(cur.fetchall())))
        for column in record:
            query2 = ("SELECT * FROM bank_db.transaction WHERE clientID = '%s'" % (column[0]))
            cur.execute(query2)
            record2 = cur.fetchall()
            for column2 in record2:
                self.ADestID.append(column2[6])  # list with client id
                self.Aamount.append(column2[2])#amount
                self.Aavg.append(column2[11])# AvgAmountOfTransaction
                self.Alocation.append(column2[12])
                self.ADestname.append(column2[13])  # list with names

        riskFlag = 0

    #This method is responsible for checking the business rules
    #Multi Criteria Decision Making

    def multi_criteria(self,name_Dest):

        flag = 0
        flag1 = 0
        flag2 = 0
        flag3 = 0
        count = 0
        average_transactions = 0

        # Read Sanctions list for Business Rule #1
        data_path2 = "Sanctions_list.csv"
        Z = pandas.read_csv(data_path2, sep=",", header=0, engine='python')
        Z = Z.as_matrix()
        # print("Read Sanctions_list")
        Sanctions_list = []
        for a in range(Z.shape[0]):
            Sanctions_list.append(Z[a, 0])

        # Read High risk countries for Business rule #2
        data_path = "HighRiskLocation.csv"
        X = pandas.read_csv(data_path, sep=",", header=0, engine='python')
        X = X.as_matrix()
        # print("Read dataset HighRiskLocation ")
        HighRiskLocation = []
        for n in range(X.shape[0]):  # Locations loop
            HighRiskLocation.append(X[n, 0])

        # Business Rule#1
        if name_Dest in self.ADestID:  # foreach???
            i = self.ADestID.index(name_Dest)  # finding the location of the id will give us the location of the name.
            if self.ADestname[i] in Sanctions_list:
                flag = 1
            # print("Sanctions_list flag", ADestID[i], flag, "*******", ADestname[i])

            # Business rule2
            if self.Alocation[i] in HighRiskLocation:
                flag1 = 1
            #  print("Location Risk", Alocation[i], flag1)

            # Busienss Rule#3 Customer risk  
            if (self.Aamount[i] > 200000):
                flag2 = 1
            #  print(Aamount[i],"amount risk", flag2)

            if self.Aamount[i] > self.Aavg[i] * 1.5:
                flag3 = 1
            #  print(Aamount[i],"average_transactions risk",Aavg[i]* 1.5)

        #print("1->", flag, "2->", flag1, "3->", flag2, "4->", flag3)
        return (flag + flag1 + flag2 + flag3) / 4

