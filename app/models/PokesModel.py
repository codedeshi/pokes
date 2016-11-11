from system.core.model import Model

class PokesModel(Model):
	def __init__(self):
		super(PokesModel, self).__init__()

	def poked_by_id(self,user_id):
		query = "select us.alias as poked_by, p.count from pokes p left join users us on p.poked_by_id = us.id where poked_id =:user_id order by p.count desc"
		poke_data = self.db.query_db(query, {'user_id': user_id})
		return poke_data

	def getusers(self, user_id):
		query = "select u.id, u.name, u.alias, u.email, coalesce(sum(p.count),0) as pokes from users u left join pokes p on p.poked_id = u.id where u.id !=:user_id group by alias"
		return self.db.query_db(query, {'user_id': user_id})

	def poke(self,poked_id,poked_by_id):
		query = "select count(id) as count from pokes where poked_id =:poked_id and poked_by_id=:poked_by_id"
		count = self.db.query_db(query, {'poked_id': poked_id, 'poked_by_id':poked_by_id})[0]['count']
		data = {
				'poked_by_id': poked_by_id,
				'poked_id': poked_id,
				'count': 1
			}
		if count == 0:
			query = 'insert into pokes (poked_by_id,poked_id,count) values (:poked_by_id,:poked_id,:count)'
			self.db.query_db(query, data)
		else:
			query = "select count from pokes where poked_id =:poked_id and poked_by_id=:poked_by_id"
			count = self.db.query_db(query, {'poked_id': poked_id, 'poked_by_id':poked_by_id})[0]['count']
			data['count'] = count+1
			query = "UPDATE pokes SET updated_at=NOW(),count=:count WHERE poked_by_id=:poked_by_id and poked_id=:poked_id;"
			self.db.query_db(query, data)
		query = 'select sum(count) from pokes where poked_id =:poked_id'
		return self.db.query_db(query, data)
