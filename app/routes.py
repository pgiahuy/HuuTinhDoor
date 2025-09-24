from flask import Blueprint, render_template
from .models import Product

main = Blueprint('main', __name__)

@main.route('/')
def index():
    products = Product.query.all()  # lấy sản phẩm từ DB Workbench
    return render_template('index.html', products=products)

@main.route('/tu_nhom')
def tu_nhom():
    return render_template('tu_nhom.html')
@main.route('/cua_nhom')
def cua_nhom():
    return render_template('cua_nhom.html')
@main.route('/lien_he')
def lien_he():
    return render_template('lien_he.html')
@main.route('/kinh_cuong_luc')
def kinh_cuong_luc():
    return render_template('kinh_cuong_luc.html')
@main.route('/san_pham')
def san_pham():
    return render_template('san_pham.html')

@main.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get(product_id)
    if not product:
        return "Sản phẩm không tồn tại", 404
    
    # # Lấy sản phẩm liên quan (cùng category, khác id)
    # related_products = Product.query.filter(
    #     Product.category_id == product.category_id,
    #     Product.id != product.id
    # ).limit(4).all()   # lấy 4 sp liên quan
    
    return render_template('product_detail.html', product=product)#, related_products=related_products)

