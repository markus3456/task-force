import manage 

database = 'postgresql://postgres:admin@localhost:5432/taskforce'
email = 'mf14@mail.com'

manage.activate_user(database,email)

