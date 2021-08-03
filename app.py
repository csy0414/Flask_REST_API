from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = "csy-dev"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///companies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Locales(db.Model):
    __table_name__ = "locales"

    id = db.Column(db.Integer, primary_key=True)
    local_name = db.Column(db.String(64), unique=True, nullable=False)
    local_code = db.Column(db.String(5), unique=True, nullable=False)

    company = db.relationship('company_translation')
    tag = db.relationship('tag_translation')

    def __init__(self, id, local_name, local_code):
        self.id = id
        self.local_name = local_name
        self.local_code = local_code

    def __repr__(self):
        return f"<Locales('{self.id}', '{self.local_name}', '{self.local_code}')>"


class Companies(db.Model):
    __table_name__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    company_tags = db.Column(db.String(255))
    company = db.relationship('company_translation', backref=db.backref('company_set'))

    def __init__(self, id, company_tags):
        self.id = id
        self.company_tags = company_tags

    def __repr__(self):
        return f"<Companies('{self.id}', '{self.company_tags}')>"


class Tags(db.Model):
    __table_name__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    tag_data = db.Column(db.String(255), unique=True, nullable=False)
    tag_value = db.relationship('tag_translation', backref=db.backref('tag_value'))

    def __init__(self, id, tag_data):
        self.id = id
        self.tag_data = tag_data

    def __repr__(self):
        return f"<Tags('{self.id}', '{self.tag_data}')>"


class CompanyTranslations(db.Model):
    __table_name__ = "company_translation"

    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), primary_key=True)
    local_id = db.Column(db.Integer, db.ForeignKey('locales.id'), primary_key=True)
    company_name = db.Column(db.String(255))


class TagTranslations(db.Model):
    __table_name__ = "tag_translation"

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    local_id = db.Column(db.Integer, db.ForeignKey('locales.id'), primary_key=True)
    tag_name = db.Column(db.String(255))

