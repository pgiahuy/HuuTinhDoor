from . import db

class Product(db.Model):
    __tablename__ = 'products'   
    id = db.Column('idproduct',db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)
    type = db.Column(db.String(255))
    description = db.Column(db.Text)
    images = db.relationship('ProductImage', backref='product', lazy=True)

class ProductImage(db.Model):
    __tablename__ = 'product_images'
    id = db.Column('id',db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.idproduct'))
    url = db.Column(db.String(255))
    alt_text = db.Column(db.String(255))
    is_main = db.Column(db.Boolean)
