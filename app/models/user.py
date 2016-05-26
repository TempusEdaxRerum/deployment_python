from system.core.model import Model
import re

class user(Model):
    def __init__(self):
        super(user, self).__init__()

    def register(self, info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        PASSWORD_REGEX = re.compile(r'^([^0-9]*|[^A-Z]*)$')
        errors = []
        if len(info['name']) < 2:
            errors.append("Invalid  Name. (Letters only, at least 2 characters.)")
        if len(info['alias']) < 2 or not info['alias'].isalpha():
            errors.append("Invalid Alias. (Letters only, at least 2 characters.)")   
        if len(info['email']) < 1 or not EMAIL_REGEX.match(info['email']):
            errors.append ("Invalid Email Address!")    
        if len(info['password']) < 8 :
            errors.append("Password should be more than 8 characters")
        if info['password'] != info['confirm_password']:
            errors.append('Password and confirm password must match!')
        if PASSWORD_REGEX.match(info['confirm_password']):
            errors.append("Password requires to have at least 1 uppercase letter and 1 numeric value ")   
        # if info['bday'] 
        #     errors.append("Please select date of birth")
        if errors:
            return {"status":False, "errors":errors}            
        else:  
            query = "INSERT into users (name, alias, email, pw_hash, created_at, updated_at) VALUES(:name,:alias,:email,:password, NOW(),NOW())"
            data = {'name': info['name'], 'alias': info['alias'], 'email' :info['email'], 'password' :info['password']}
            self.db.query_db(query, data)
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)
            return {"status": True, "user": users[0]}


    def login(self,info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        if len(info['email']) < 1 or not EMAIL_REGEX.match(info['email']):
            errors.append ("Invalid Email Address!")    
        if len(info['password']) < 8 :
            errors.append("Password should be more than 8 characters")
            #if we have error, we will return  false and errors will be carried to controller.
        if errors:
            return {"status":False, "errors":errors}            
        else:  
            query = "SELECT * FROM users WHERE email = :email LIMIT 1"
            data = {'email' : info['email']}
            users = self.db.query_db(query,data) 
            return {"status": True, "user": users[0]}

    def list_of_quotes(self, info):
        print info
        print "&"*40
        query="SELECT quotes.id as quotes_id, quotes.quote as quote, users.name as name, quotes.created_at as created_on , quotes.user_id as quote_user_id from quotes left join users on users.id = quotes.user_id WHERE NOT quotes.id IN (SELECT quotes.id from quotes LEFT JOIN users ON users.id = quotes.user_id LEFT JOIN favorites on favorites.quote_id = quotes.id WHERE favorites.user_id = :id)"
        data={
            'id': info
        }

        return self.db.query_db(query, data)

    def favorite_quotes(self, info):
        query="SELECT quotes.id as quote_id, users.id as poster_id, users.name as name, quote from quotes LEFT JOIN users ON users.id = quotes.user_id LEFT JOIN favorites on favorites.quote_id = quotes.id WHERE favorites.user_id = :id" 
        data={
            'id': info
        } 
        return self.db.query_db(query, data) 

    def create_favorite(self, info):
        query = "INSERT INTO favorites (user_id, quote_id, updated_at, created_at) VALUES (:user_id ,:quote_id , NOW(), NOW());"
        print "hello"
        data = {'user_id': info['user_id'], 'quote_id':info['quotes_id']}
        print "goodbye"
        return self.db.query_db(query, data)

    def create_quote(self, info):
        query = "insert into quotes (quote, user_id, created_at, updated_at) values (:quote, :user_id ,now(),now())"
        print "HELLLLO"
        data = {'quote': info['quote'], 'user_id': info['user_id']}
        print "GOOODBYE"
        return self.db.query_db(query, data)


    def users_page(self, info):
        query= "select users.name as name, alias, email, count(quotes.user_id) as count, quotes.quote as quotes, quotes.id as quotes_id from users left join quotes on quotes.user_id = users.id where users.id = :id"   
        data =  {"id" : info }
        return self.db.query_db(query, data)





