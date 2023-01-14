import psycopg2

def deploy():
	"""Run deployment tasks."""
	from app import create_app,db
	#from flask_migrate import upgrade,migrate,init,stamp
	from models import User

    

	app = create_app()
	app.app_context().push()
	db.create_all()

	# migrate database to latest revision
	#init()
	#stamp()
	#migrate()
	#upgrade()
	print("database deployed")
deploy()

def activate_user(database,email):
	conn_string = database
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()

	query = '''UPDATE user2 SET activate = true WHERE email = '{}'
	'''.format(email)
    
	cursor.execute(query)
	updated_rows = cursor.rowcount
	print(updated_rows)
	conn.commit()
	cursor.close()

def add_column(database,table_name,column_name):
	#connect to db
	conn_string = database
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	print(f'opend {conn_string} successful')


	query = f'''ALTER TABLE {table_name} ADD COLUMN {column_name} float'''
	cursor.execute(query)
	print(f"column: {column_name} added")
	conn.commit()
	cursor.close()

# db = 'postgresql://postgres:postgres@localhost:5455/mytest'
# tn = 'fake_tasks'
# cn = 'hours_worked' 
# add_column(db,tn,cn)
