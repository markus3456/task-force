import sqlalchemy
from sqlalchemy import select
import pandas as pd




def table_of_tasks(user_id):

    engine = sqlalchemy.create_engine('postgresql://postgres:postgres@localhost:5455/mytest' )


    query =''' WITH tab1 AS(SELECT  task_id, AGE(stop,start) AS hours 
                FROM hours),
                tab2 AS(SELECT task_id, total_hours 
                    FROM (SELECT task_id, sum(hours) OVER (PARTITION BY task_id ORDER BY hours) AS total_hours 
                        FROM tab1 ) AS e)
                SELECT t.id, t.title , t.category, t.createtime, t.completetime, t.complete, max(total_hours) AS max_hours 
                FROM fake_tasks t
                LEFT JOIN tab2 h 
                ON h.task_id = t.id
                WHERE user_id = {}
                GROUP BY id  ,title  , category  
                ORDER BY id
                ;'''.format(user_id)

    df = pd.read_sql(query,  con = engine)
    print(df)
    return query

