from . import db
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

# --- CATEGORY / SUBCATEGORY ---

class Category(db.Model):
    __tablename__ = 'category'
    id =db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(100), nullable=False)
    subcategories = db.relationship('SubCategory',  backref='category', lazy=True, cascade="all, delete-orphan")

class SubCategory(db.Model):
    __tablename__ = 'subcategory'
    id = db.Column(db.Integer, primary_key=True)  # tự tăng
    name = db.Column(db.String(100), nullable=False)  # Ví dụ: Cửa gỗ, Cửa kính
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    products = db.relationship('Product', backref='subcategory', lazy=True, cascade="all, delete-orphan")

# --- PRODUCT ---
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False) 
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=False)  
    description = db.Column(db.Text)
    images = db.relationship('ProductImage', backref='product', lazy=True, cascade="all, delete-orphan")

class ProductImage(db.Model):
    __tablename__ = 'product_images'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    public_id = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255))
    alt_text = db.Column(db.String(255))
    is_main = db.Column(db.Boolean)

# --- PROJECT ---
class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    images = db.relationship("ProjectImage", backref="project", lazy=True, cascade="all, delete-orphan")


class ProjectImage(db.Model):
    __tablename__ = 'project_images'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    public_id = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255))
    alt_text = db.Column(db.String(255))
    is_main = db.Column(db.Boolean)

# --- FORMS ---
class ProductForm(FlaskForm):
    name = StringField('Tên sản phẩm', validators=[DataRequired()])
    price = FloatField('Giá', validators=[DataRequired()])
    category = SelectField('Danh mục', coerce=int, validators=[DataRequired()])
    subcategory = SelectField('Loại sản phẩm', coerce=int, validators=[DataRequired()])
    description = TextAreaField('Mô tả')
    submit = SubmitField('Thêm sản phẩm')

class ProjectForm(FlaskForm):
    name = StringField('Tên dự án', validators=[DataRequired()])
    description = TextAreaField('Mô tả')
    submit = SubmitField('Thêm dự án')
