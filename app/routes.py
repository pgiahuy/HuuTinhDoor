from flask import Blueprint, render_template
from .models import Product

main = Blueprint('main', __name__)

@main.route('/')
def index():
    products = Product.query.all()  # lấy sản phẩm từ DB Workbench
    return render_template('index.html', products=products)
