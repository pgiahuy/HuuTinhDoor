from . import db
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class Product(db.Model):
    __tablename__ = 'product'   
    id = db.Column('id',db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)
    category_id = db.Column(db.String(255))
    description = db.Column(db.Text)
    images = db.relationship('ProductImage', backref='product', lazy=True)

class ProductImage(db.Model):
    __tablename__ = 'product_images'
    id = db.Column('id',db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    url = db.Column(db.String(255))
    alt_text = db.Column(db.String(255))
    is_main = db.Column(db.Boolean)
    
class Project(db.Model):
    __tablename__ = 'project'   
    id = db.Column('id',db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    images = db.relationship('ProjectImage', backref='project', lazy=True)

class ProjectImage(db.Model):
    __tablename__ = 'project_images'
    id = db.Column('id',db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    url = db.Column(db.String(255))
    alt_text = db.Column(db.String(255))
    is_main = db.Column(db.Boolean)
    
    
#add form
class ProductForm(FlaskForm):
    name = StringField('Tên sản phẩm', validators=[DataRequired()])
    price = FloatField('Giá', validators=[DataRequired()])
    category_id = StringField('Category ID', validators=[DataRequired()])
    description = TextAreaField('Mô tả')
    submit = SubmitField('Thêm sản phẩm')

class ProjectForm(FlaskForm):
    name = StringField('Tên dự án', validators=[DataRequired()])
    description = TextAreaField('Mô tả')
    submit = SubmitField('Thêm dự án')
