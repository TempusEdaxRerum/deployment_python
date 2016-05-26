from system.core.router import routes


routes['default_controller'] = 'users'
routes['POST']['/register'] =  'users#register'
routes['POST']['/login'] = 'users#login'
routes['/quotes'] = 'users#showquotes'
routes['GET']['/logout'] = 'users#logout'
routes['POST']['/addfavorite'] = 'users#addfavorite'
routes['POST']['/newquote'] = 'users#newquote'
routes['/users/<quote_user_id>'] = 'users#show_users'