from datetime import datetime
from flask import flash
from app.models.connection import connectToMySQL


create_table = '''
create table if not exists quotes  (
    id int auto_increment primary key,
    autor varchar(45) not null,
    message varchar(255) not null,
    creator_id int not null,
    foreign key (creator_id) references users(id)
)
'''
connectToMySQL().query_db(create_table)

middle_table = '''
create table if not exists users_quotes  (
    user_id int not null,
    quote_id int not null,
    primary key(user_id, quote_id),
    foreign key (user_id) references users(id) on delete cascade,
    foreign key (quote_id) references quotes(id) on delete cascade
)
'''
connectToMySQL().query_db(middle_table)


class Quote:

    def __init__(self, data):
        self.id = data['id']
        self.message = data['message']
        self.creator_id = data['creator_id']


    @staticmethod
    def validate(form):
        is_valid = True
        # 1. validamos el nombre
        
        
        if len(form['autor']) < 2:
            flash('El nombre debe tener al menos 2 caracteres', 'error')
            is_valid = False
        
        if len(form['mensaje']) < 10:
            flash('el mensaje debe tener al menos 10 caracteres', 'error')
            is_valid = False
            
        return is_valid


    @classmethod
    def create(cls, autor, message, creator_id):
        #import pdb; pdb.set_trace()
        query = '''
            insert into quotes (autor, message, creator_id) values (%(autor)s, %(message)s, %(creator_id)s)
        '''
        data = {
            'autor' : autor,
            'message': message,
            'creator_id': creator_id
        }
        print(data)
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        new_quote_id = connectToMySQL().query_db(query, data)

        query2 = '''
            insert into users_quotes (user_id, quote_id) values (%(creator_id)s, %(quote_id)s)
        '''
        data2 = {
            'creator_id': creator_id,
            'quote_id': new_quote_id
        }

        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        new_quote_id = connectToMySQL().query_db(query2, data2)
        
        flash('Comentario creado con éxito', 'success')


    @classmethod
    def favorites(cls, user_id):
        # Comentarios favoritos
        query = '''
            select * from quotes join users_quotes
            on quotes.id = users_quotes.quote_id
            where user_id = %(user_id)s
            
        '''
        data = {
            'user_id': user_id,
        }
        results = connectToMySQL().query_db(query, data)
        return results

    @classmethod
    def quotable_quotes(cls, user_id):
        # comentarios No favoritos
        query = '''
            select * from quotes
            where id not in 
                (select id from quotes join users_quotes
                on quotes.id = users_quotes.quote_id
                where user_id = %(user_id)s)
            
        '''
        data = {
            'user_id': user_id,
        }
        results = connectToMySQL().query_db(query, data)
        return results

    @classmethod
    def join_quote(cls, user_id, quote_id):
        query = '''
            insert into users_quotes (user_id, quote_id)
            values (%(user_id)s, %(quote_id)s)
        '''
        data = {
            'user_id': user_id,
            'quote_id': quote_id
        }
        results = connectToMySQL().query_db(query, data)
        return results

    @classmethod
    def drop_quote(cls, user_id, quote_id):
        query = '''
            delete quote from users_quotes
            where user_id = %(user_id)s and quote_id = %(quote_id)s
        '''
        data = {
            'user_id': user_id,
            'quote_id': quote_id
        }
        results = connectToMySQL().query_db(query, data)
        return results

    @classmethod
    def edit_quote(cls, message, autor, quote_id):
        query = '''
            update quotes 
            set message = %(message)s, autor = %(autor)s
            where id = %(quote_id)s 
        '''
        data = {
            'message': message,
            'autor': autor,
            'quote_id': quote_id
        }
        results = connectToMySQL().query_db(query, data)
        return results
