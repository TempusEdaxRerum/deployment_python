from system.core.controller import *

class users(Controller):
    def __init__(self, action):
        super(users, self).__init__(action)
        self.load_model('user')
        self.db = self._app.db

    def index(self):
        return self.load_view('login.html')

    def register(self):
        user_info = self.models['user'].register(request.form)
        if user_info['status'] == True:
            session['id'] = user_info['user']['id'] 
            session['name'] = user_info['user']['name']            
            return redirect ('/quotes')
        else:
            for message in user_info['errors']:
                flash(message)
            return redirect('/')

    def login(self):
        login_info = self.models['user'].login(request.form)
        print login_info
        if login_info['status'] == True:
            session['id'] = login_info['user']['id'] 
            session['name'] = login_info['user']['name']
            return redirect('/quotes')
        else:
            #for all errors from model page flash on page.
            for message in login_info['errors']:
                flash(message)
            return redirect('/')

    def showquotes(self):
        
        quote_list = self.models['user'].list_of_quotes(session['id'])
        favorite_quote = self.models['user'].favorite_quotes(session['id'])
        return self.load_view('quotes.html', quote_list = quote_list, favorite_quote = favorite_quote)

    def logout(self):
        del session['id']
        del session['name']
        return redirect('/')

    def addfavorite(self):
        print request.form['quotes_id']
        print "*"*50
        newreview = {'quotes_id': request.form['quotes_id'], 'user_id': session['id']}
        self.models['user'].create_favorite(newreview)
        return redirect ('/quotes')

    def newquote(self):
        newreview = {'quote': request.form['addquote'], 'user_id': session['id']}
        newquote = self.models['user'].create_quote(newreview)
        return redirect ('/quotes')

    def show_users(self, quote_user_id):
        user_info = self.models['user'].users_page(quote_user_id)
        return self.load_view('users.html', user_info = user_info)


