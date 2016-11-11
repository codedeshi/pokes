from system.core.router import routes

routes['default_controller'] = 'Welcome'
routes['POST']['/registration'] = 'Welcome#registration'
routes['POST']['/login'] = 'Welcome#login'
routes['/profile'] = 'Pokes#profile'
routes['POST']['/poke/<poked_id>'] = 'Pokes#poke'
 