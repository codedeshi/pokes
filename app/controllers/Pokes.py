from system.core.controller import *

class Pokes(Controller):
	def __init__(self, action):
		super(Pokes, self).__init__(action)
		self.load_model('PokesModel')

	def profile(self):
		if session['user'] != None:
			poke_data = self.models['PokesModel'].poked_by_id(session['user']['id'])
			others_data = self.models['PokesModel'].getusers(session['user']['id'])
			pokers = len(poke_data)
			return self.load_view('profile.html', others_data = others_data, user=session['user'], poke_data=poke_data, pokers=pokers)

	def poke(self,poked_id):
		if session['user'] != None:
			self.models['PokesModel'].poke(poked_id,session['user']['id'])
			return redirect('/profile')
		else:
			return redirect('/')