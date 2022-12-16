import manage 

database = 'dbname=mytest user=postgres host=myPostgresDB password=postgres port=5455'
email = 'mf14@mail.com'

manage.activate_user(database,email)

