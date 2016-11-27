from system.core.model import Model
import re

class WelcomeModel(Model):
	def __init__(self):
		super(WelcomeModel, self).__init__()

	def register(self, data):
		EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
		error = []
		if len(data['name']) < 3:
			error.append("Name should be atleast 3 characters")
		if len(data['alias']) < 3:
			error.append("Alias should be atleast 3 characters")
		if not EMAIL_REGEX.match(data['email']):
			error.append('Invalid Email')
		if len(data['password']) < 8:
			error.append("Password should be atleast 8 characters")
		if data['password'] != data['confirm']:
			error.append('Password and confirm pw should match')


		if error:
			return {'status': False , 'error': error}
		else:
			try:
				query = "INSERT into users (name, alias,email ,password) values (:name, :alias, :email, :password)"
				data['password'] = self.bcrypt.generate_password_hash(data['password'])
				user_id = self.db.query_db(query, data)        
				return {'status': True, "user_id": user_id}
			except Exception as e:
				error.append('Alias or Email already exists')
				return {'status': False , 'error': error}

	def login(self,data):
		query = "SELECT * from users where email=:email"
		user_data = self.db.query_db(query, data)
		if len(user_data)==1:
			if self.bcrypt.check_password_hash(user_data[0]['password'], data['password']):
				return user_data[0]
			else:
				return False
		return False

	def get_user(self,user_id):
		query = 'select * from users where id = :user_id'
		user = self.db.query_db(query, {'user_id': user_id})
		if len(user)==1:
			return user[0]


