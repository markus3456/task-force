import pandas as pd
import numpy as np
import faker
from datetime import datetime, timedelta
import random
import psycopg2

fake = faker.Faker()

def make_tasks(num):

    #create lists to choose data from
    array = np.arange(1,1,0.05)
    category_list = ["programming", "art", "sport"]
    title_list = ["drink coffee", "produce shitty code", "lay in bed", "count leaves of trees", "count sand on the beach",
                "buy socks","buy pants","eat","sleep","nap", "brush your teeth", "get dressed", "go for a walk"]
    
  
    # base = todays time
    base = pd.Timestamp.today()

    # todays time + 12 hours (12h time to complete)
    base2 = pd.Timestamp.today() + timedelta(days=0.5)
    

    
    fake_tasks = [{ 'id':x+1,
                    'title': np.random.choice(title_list),
                    'category': np.random.choice(category_list),
                    'createtime': base + timedelta(days=x),
                    'completetime': base2 + timedelta(days=x) + timedelta(days=random.uniform(0,1)),
                    'complete':    pd.Series([True]).bool()} for x in range(num)]
    fake_tasks = pd.DataFrame(fake_tasks)
    return fake_tasks




def upload_db(df):
    #replace df data types with sql datatypes
    replacements = {
        'object': 'varchar',
        'float64': 'float',
        'int64': 'int',
        'datetime64[ns]': 'timestamp',
        'timedelta64[ns]': 'varchar',
        'bool': 'boolean'
    }
    print(replacements)

    col_str = ", ".join("{} {}".format(n,d) for (n,d) in zip(df.columns, df.dtypes.replace(replacements)))
    print(col_str)

    #connect to database
    conn_string = 'postgresql://postgres:admin@localhost:5432/taskforce'
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('opend db successfully')
    
    #drop existing tables
    cursor.execute("drop table if exists fake_tasks;")

    #create table
    #create a Primary key with nextval sequence in order to enable adding ids sequentially (aviod adding ids with same value)
    #it might happen that sequence and the number of ids is out of sync upfront. 
    #In this case we have to sync the sequence with following command:
    #SELECT setval('tasks_id_seq', (SELECT MAX(id) FROM fake_tasks)+1);
    cursor.execute("create table fake_tasks \
        (id int PRIMARY KEY DEFAULT NEXTVAL('tasks_id_seq'), title varchar, category varchar, createtime timestamp, completetime timestamp,  complete boolean)")
    
    #insert values to table by saving df to csv in temp folder and upload to db
    df.to_csv('fake_tasks.csv', header=df.columns, index=False, encoding='utf-8')
    my_file = open('fake_tasks.csv')

    SQL_STATEMENT = """
    COPY fake_tasks FROM STDIN WITH
    CSV
    HEADER
    DELIMITER AS ','
    """
    cursor.copy_expert(sql=SQL_STATEMENT, file=my_file)
    cursor.execute("grant select on table fake_tasks to public")
    conn.commit()

    cursor.close()
    print('upload complete')
    print(len(df.index))

num = 100
task_df = make_tasks(num)
print(task_df)
print(task_df.info())

a = upload_db(task_df)