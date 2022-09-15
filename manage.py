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