import pandas



class MultiCriteria:

    #Reading from the orignal CSV
    data_path1 = "GeneratedDataset.csv"
    #print("Reading dataset")
    Y = pandas.read_csv(data_path1, sep=",",header=0)
    Y = Y.as_matrix()
    #print("Read orignal dataset")

    #col
    step = 0
    type = 1
    amount = 2
    nameOrig = 3
    oldBalanceOrig = 4
    newBalanceOrig = 5
    nameDest = 6
    oldBalanceDest = 7
    newBalanceDest = 8
    errorBalanceOrig =9
    errorBalanceDest=10
    AvgAmountOfTransaction=11
    location = 12
    clientName = 13

    riskFlag = 0
    ADestID = []
    ADestname = []
    Alocation = []
    Aamount = []
    Atype = []
    Aavg = []


    for i in range(Y.shape[0]):
        # storing data into a temprary array
        ADestID.append(Y[i,nameDest])
        ADestname.append(Y[i,clientName])
        Alocation.append(Y[i, location])
        Aamount.append(Y[i, amount])
        Atype.append(Y[i, type])
        Aavg.append(Y[i, AvgAmountOfTransaction])
        ClientID = Y[i, nameDest]

    #This method is responsible for checking the business rules
    #Multi Criteria Decision Making

    def multi_criteria(name_Dest):

        flag = 0
        flag1 = 0
        flag2 = 0
        flag3 = 0
        count = 0
        average_transactions = 0

        # Read Sanctions list for Business Rule #1
        data_path2 = "/Users/mac/Downloads/Sanctions_list.csv"
        Z = pandas.read_csv(data_path2, sep=",", header=0 , engine='python')
        Z = Z.as_matrix()
       # print("Read Sanctions_list")
        Sanctions_list=[]
        for a in range(Z.shape[0]):
            Sanctions_list.append(Z[a,0])


        # Read High risk countries for Business rule #2
        data_path = "/Users/mac/Downloads/HighRiskLocation.csv"
        X = pandas.read_csv(data_path, sep=",", header=0, engine='python')
        X = X.as_matrix()
        #print("Read dataset HighRiskLocation ")
        HighRiskLocation = []
        for n in range(X.shape[0]):  # Locations loop
            HighRiskLocation.append(X[n,0])

        # Business Rule#1
        if name_Dest in ADestID: # foreach???
            i = ADestID.index(name_Dest) #finding the location of the id will give us the location of the name.
            if ADestname[i] in Sanctions_list:
                flag = 1
               # print("Sanctions_list flag", ADestID[i], flag, "*******", ADestname[i])

        # Business rule2
            if Alocation[i] in HighRiskLocation:
                flag1 = 1
              #  print("Location Risk", Alocation[i], flag1)

        # Busienss Rule#3 Customer risk  
            if (Aamount[i] > 200000):
                flag2 = 1
                print(Aamount[i],"amount risk", flag2)

            if Aamount[i] > Aavg[i]* 1.5:
                flag3 = 1
                print(Aamount[i],"average_transactions risk",Aavg[i]* 1.5)

        print("1->",flag,"2->",flag1,"3->",flag2,"4->",flag3)
        return flag + flag1 + flag2 + flag3

explored = []
#To extract the destName
for n in range(Y.shape[0]):
    ClientID = Y[n, nameDest]
    # Flag risk is the number business rules that has been satisfied
    if ClientID not in explored:
        explored.append(ClientID)
        Flagrisk = multi_criteria(ClientID)
        print(ClientID, "\n", "Risk:", Flagrisk/4) # 4 stands for #of business rules