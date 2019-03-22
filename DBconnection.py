import mysql.connector
from sqlalchemy import create_engine

def connection2():

    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 passwd="SMIhmwn19*",
                                 db="Bank_DB",
                                 autocommit=True)
    cur = db.cursor()

    engine = create_engine("mysql+mysqlconnector://root:SMIhmwn19*@localhost/Bank_DB")

    return cur, db, engine

def SMI_engine():
    engine = create_engine("mysql+mysqlconnector://root:SMIhmwn19*@localhost/SMI_DB")

    return engine

def connection1():

    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 passwd="SMIhmwn19*",
                                 db="SMI_DB",
                                 autocommit=True)
    cur = db.cursor()

    engine = create_engine("mysql+mysqlconnector://root:SMIhmwn19*@localhost/SMI_DB")

    return cur, db, engine
