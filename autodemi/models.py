from datetime import datetime
from autodemi import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

content_tags = db.Table('content_tags',
    db.Column('content_id', db.Integer, db.ForeignKey('content.content_id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.tag_id'), primary_key=True)
)


class UserLibrary(db.Model):
    __tablename__ = 'user_library'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.content_id'), primary_key=True)
    consumed = db.Column(db.Boolean, default=False)
    to_consume = db.Column(db.Boolean, default=False)
    consuming = db.Column(db.Boolean, default=False)
    star = db.Column(db.Boolean, default=False)
    content = db.relationship("Content", back_populates="users")
    user = db.relationship("User", back_populates="library_content")

    def __repr__(self):
        return f"UserLibrary item('content_id:{self.content_id}', 'user_id:{self.user_id}')"


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    content = db.relationship('Content', backref='creator', lazy='dynamic')
    tag = db.relationship('Tag', backref='creator', lazy='dynamic')
    #library = db.relationship("Content", secondary=user_library, backref='userl')
    library_content = db.relationship("UserLibrary", back_populates="user")


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Content(db.Model):
    __tablename__ = 'content'
    content_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='unavailable.jpg')
    link = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(280), nullable=True)
    tags = db.relationship("Tag", secondary=content_tags, backref='content')
    users = db.relationship("UserLibrary", back_populates="content")

    def __repr__(self):
        return f"Content('{self.title}', '{self.date_added}')"


class Tag(db.Model):
    __tablename__ = 'tag'
    tag_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(140), nullable=True)

    def __repr__(self):
        return f"User('{self.title}', '{self.date_added}')"

