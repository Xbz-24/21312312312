# from datetime import datetime
from flask import flash
from app.models.connection import connectToMySQL
from app import bcrypt


create_table = '''
create table if not exists users  (
    id int auto_increment primary key,
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    email varchar(255) not null unique,
    password varchar(255) not null
)
'''
connectToMySQL().query_db(create_table)


class User:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def validate(cls, form):
        is_valid = True
        # 1. validamos el nombre
        if form['first_name'].strip() == '':
            is_valid = False
            flash('Debe ingresar un nombre', 'error')
        # 2. validamos el apellido
        if form['last_name'].strip() == '':
            is_valid = False
            flash('Debe ingresar un apellido', 'error')
        # 3. validamos la contraseña
        if form['password'].strip() == '':
            is_valid = False
            flash('Debe ingresar una contraseña', 'error')

        # 4. validamos que las contraseñas coincidan
        if form['password'] != form['password_confirm']:
            is_valid = False
            flash('Ambas contraseñas debe coincidir', 'error')

        # 5. validamos que no exista previamente otro usuario con el mismo email
        if not cls.check_email(form['email']):
            is_valid = False
            flash('Ese email ya se encuentra registrado', 'error')

        return is_valid

    @classmethod
    def check_email(cls, email):
        query = '''
            select * from users where email=%(email)s
        '''
        data = {
            'email': email
        }

        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL().query_db(query, data)

        if len(results) == 0:
            return True
        else:
            return False

    @classmethod
    def create(cls, first_name, last_name, email, password):
        query = '''
            insert into users (first_name, last_name, email, password) values (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        '''
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': bcrypt.generate_password_hash(password)
        }

        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        new_user_id = connectToMySQL().query_db(query, data)

        # retornamos el ID del usuario recientemente creado
        return new_user_id

    @classmethod
    def change_password(cls, email, old_password, new_password, new_password_confirm):
        # 1. Chequear que ambas contraseñas muevas coincidan
        if new_password != new_password_confirm:
            flash('Las contraseñas no coinciden', 'error')
            return

        # 2. Recupero el usuario con su contraseña antigua
        user = cls.get_with_credentials(email, old_password)
        if user is None:
            return

        # 3. Actualizo la contraseña
        query = '''update users set password=%(new_password)s  where email=%(email)s'''

        data = {
            'email': email,
            'new_password': bcrypt.generate_password_hash(new_password)
        }

        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        connectToMySQL().query_db(query, data)

        # 4. Le doy feedback al usuario
        flash('Contraseña actualizada con éxito', 'success')

    # ahora usamos métodos de clase para consultar nuestra base de datos

    @classmethod
    def get_with_credentials(cls, email, password):
        # 1. Obtenemos el usuario
        query = '''SELECT * FROM users where email=%(email)s'''

        data = {
            'email': email
        }

        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL().query_db(query, data)

        if len(results) == 0:
            flash('Email inexistente o contraseña incorrecta', 'error')
            return None

        # 2. Verificar que las contraseñas coincidan
        encriptada = results[0]['password']

        if not bcrypt.check_password_hash(encriptada, password):
            flash('Email inexistente o contraseña incorrecta', 'error')
            return None

        # si llegamos hasta acá, todo está OK
        return cls(results[0])
