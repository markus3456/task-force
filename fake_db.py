
import pandas as pd
import numpy as np
import datetime
import psycopg2
import sys
import random


def create_db():
  
    #connect to database
    conn_string = 'postgresql://postgres:admin@localhost:5432/taskforce'
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('opend db successfully')
    
    #drop existing tables
    cursor.execute("drop table if exists fakedb;")

    #create table
    cursor.execute("create table fakedb \
        (id integer, titel varchar, category varchar, createtime timestamp, completetime timestamp, complete boolean)")
    cursor.execute("create sequence tasks_id_seq;")
    cursor.execute("grant select on table fakedb to public")
    conn.commit()

    cursor.close()


  
n_days = 100
  
# today's date in timestamp
base = pd.Timestamp.today()
  
# calculating timestamps for the next 10 days
createtime_list = [base + datetime.timedelta(days=x) for x in range(n_days)]
#.replace(second = 0, microsecond=0)
# iterating through timestamp_list
for x in createtime_list:
    print(x)

n_days = 100
  
# today's date in timestamp
base = pd.Timestamp.today() + datetime.timedelta(days=0.5)
  
# calculating timestamps for the next 10 days
completetime_list = [base + datetime.timedelta(days=x) for x in range(n_days)]
#.replace(second = 0, microsecond=0)
# iterating through timestamp_list
for x in completetime_list:
    print(x)





conn_string = 'postgresql://postgres:admin@localhost:5432/taskforce'
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
print('opend db successfully')



cursor.execute("drop table if exists fakedb;")

#create table
cursor.execute("create table fakedb \
    (id integer PRIMARY KEY, titel varchar, category varchar, createtime timestamp, completetime timestamp, complete boolean)")

cursor.execute("grant select on table fakedb to public")



array = np.arange(1,101,1)
category_list = ["programming", "art", "sport"]
title_list = ["drink coffee", "produce shitty code", "lay in bed", "count leaves of trees", "count sand on the beach",
"but socks","buy pants","eat","sleep","nap", "brush your teeth", "get dressed", "go for a walk"
]
print(array)


class GenerateData:

#generate a specific number of records to a target table in the
#postgres database.

    def __init__(self):
    
        #define command line arguments.
    
        self.table = sys.argv[1]
        self.num_records = int(sys.argv[2])
        
    def create_data(self):
        """
        using the faker library, generate data and execute DML.
        """
        

        if self.table == "fakedb":
            with cursor.begin() as conn:
                for _ in range(self.num_records):
                    insert_stmt = fakedb.insert().values(
                        id = array,
                        title = random.choice(title_list),
                        category = random.chioice(category_list),
                        createtime = createtime_list,
                        completetime = completetime_list,
                        complete = fakedb.complete
                    )
                    conn.execute(insert_stmt)
       
if __name__ == "__main__":    
    generate_data = GenerateData()   
    generate_data.create_data()


#a = create_db()


