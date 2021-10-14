import re
import bcrypt
from flask_bcrypt import generate_password_hash,check_password_hash
import datetime
from app.db import db
from sqlalchemy import Table, ForeignKey, Column, Integer, String, DateTime, Boolean, text, select, and_
from sqlalchemy.orm import relationship
from app.models.rol import Rol


user_roles = Table('usuario_tiene_rol',db.Model.metadata,
    Column('usuarios_id',ForeignKey('usuarios.id'),primary_key=True),
    Column('roles_id',ForeignKey('roles.id'),primary_key=True))


class User(db.Model):
    @classmethod
    def login(cls, params):
        print()
        user=User.query.filter(User.email == params["email"]).first()
        if user and not user.deleted and user.active and user.verify_password(params["password"]):
            return user
        return None

    @classmethod
    def get_permissions(cls, user_id):
        sql = text("SELECT p.name \
                FROM usuarios u  \
                INNER JOIN usuario_tiene_rol utr ON(utr.usuarios_id = u.id) \
                INNER JOIN roles r ON(r.id = utr.roles_id) \
                INNER JOIN rol_tiene_permiso rtp ON (rtp.roles_id = r.id) \
                INNER JOIN permisos p ON (p.id = rtp.permisos_id) \
                WHERE u.id = :user_id")
        permissions = [elem[0] for elem in db.session.execute(sql, {"user_id": user_id})]
        return permissions

    @classmethod
    def has_permission(cls, user_id, permission):
        return permission in User.get_permissions(user_id)
    
    @classmethod
    def get_id_from_email(cls, user_email):
        sql = text("SELECT id \
                    FROM usuarios \
                    WHERE email = :user_email")
        id = list(db.session.execute(sql, {"user_email": user_email})) 
        return id[0][0]

    @classmethod
    def exists_user(cls, params):
        user = User.query.filter((User.email == params["email"]) | (User.username == params["username"])).first()
        return user
    
    @classmethod
    def exists_user_with_username(cls, username):
        return User.query.filter(User.username == username).first()
    
    @classmethod
    def exists_user_with_email(cls, email):
        return User.query.filter(User.email == email).first()

    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(255))
    lastname = Column(String(255))
    username = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    password_hash = Column(String(128))
    roles = relationship("Rol",secondary='usuario_tiene_rol', back_populates='users')
    active = Column(Boolean, default=True)
    deleted = Column(Boolean, default=False)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow,default=None)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


    def __init__(self, email, password, username ,roles=None, firstname=None, lastname=None):
        self.email = email
        self.password_hash = generate_password_hash(password).decode('utf-8')
        self.username = username
        self.firstname = firstname
        self.lastname = lastname

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password) 

    def get_user_by_id(id):
        return User.query.filter(User.id==id).first()


    def get_user_by_email(email):
        return User.query.filter(User.email==email).first()


    def get_user_by_username(username):
        return User.query.filter(User.username==username).first()

        
    def get_index_users(id, page, config):
        return User.query.filter(User.deleted==False).filter(User.id != id).order_by(User.id.asc()).paginate(page, per_page=config.elements_per_page)
