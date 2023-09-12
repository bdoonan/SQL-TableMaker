import json
import psycopg2
#program to psogtresql to make a table based on the data in a json file
#I wanted to make it so that it could generate the table for any number of keys,
#but this does not work with the insert command, so I made it for a
#2 column table only but the code is easily alterable for any number of columns
def insertData():
        dbHost = input("What is the name of the server for your database? If local type localhost\n")
        db = input("What is the name of your database?\n")
        dbUser = input("What is username for the user of your database?\n")
        dbPass = input("What is this user's password?\n") 

        conn = psycopg2.connect(host=dbHost, database = db, user = dbUser, password=dbPass)
        cur = conn.cursor()
        #This commented code makes it quicker to check if the database is made
        #cur.execute("set search_path to public")
        print("Connected to database")
        
        fileName = input("What is the name of the json file?\n")
        jsonString=".json"
        if jsonString not in fileName:
                fileName = fileName+jsonString
        with open(fileName) as file:
                data = json.load(file)
        print("File loaded")
        
        sqlTable = input("What do you want the name of your table to be?\n")
        #numberOfKeys = int(input("How many keys will be in your table?\n"))
        #This is where you would change based on the number of keys 
        numberOfKeys=2
        Keys = [0]*numberOfKeys
        KeyData = [0]*numberOfKeys
        KeyType = [0]*numberOfKeys
        
        Keys[0] = input("What is the name of your primary key?\n")
        KeyData[0] = input("What is the name of this data parameter for this key in the json file\n")
        KeyType[0] = input("What is the type of the primary key\n")
        for i in range(numberOfKeys-1):
                Keys[i+1]=input("What is the name of this next key?\n")
                KeyData[i+1]=input("What is the name of this data parameter for this key in the json file\n")
                KeyType[i+1] = input("What is the type of this key\n")
       
        cur.execute(" DROP TABLE  if exists " + sqlTable)
        cur.execute(""" CREATE TABLE """ + sqlTable + """(
                        """ + Keys[0] + " " + KeyType[0] + " PRIMARY KEY) """)
        for j in range(numberOfKeys-1):
                cur.execute(""" ALTER TABLE """ + sqlTable + """\
                                ADD """ + Keys[j+1] + " " + KeyType[j+1])
        
                for data in data:
                        cur.execute("INSERT INTO " + sqlTable + " (" + Keys[0]+ ", " + Keys[1]+") VALUES (%s,%s)", (data[KeyData[0]], data[KeyData[1]]))
                
                        #cur.execute("INSERT INTO " + sqlTable + " (" + Keys[i]+") VALUES (%s)", ([data[KeyData[i]]]))
        print("Table created")
        conn.commit()
        conn.close()
insertData()
