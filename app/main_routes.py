from flask import Blueprint, render_template, jsonify,send_from_directory,Flask
from .models import Product,Project


main = Blueprint('main', __name__, static_folder='static')



@main.route('/')
def index():
    return main.send_static_file('index.html')

# API trả cả product và project cùng lúc
@main.route('/api/index')
def api_index():
    products = Product.query.all()
    projects = Project.query.all()

    products_list = [{k: v for k, v in p.__dict__.items() if k != '_sa_instance_state'} for p in products]
    projects_list = [{k: v for k, v in pr.__dict__.items() if k != '_sa_instance_state'} for pr in projects]

    return jsonify({
        'products': products_list,
        'projects': projects_list
    })
@main.route('/api/products')
def api_products():
    products = Product.query.all()
    products_list = []
    for p in products:
        # Lấy ảnh chính nếu có
        images = [{"url": img.url, "alt_text": img.alt_text, "is_main": img.is_main} for img in p.images]

        # Lấy tên category/subcategory
        category_name = p.category.name if hasattr(p, 'category') and p.category else "Chưa xác định"
        subcategory_name = p.subcategory.name if hasattr(p, 'subcategory') and p.subcategory else "Chưa xác định"

        products_list.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "category_id": p.category_id,
            "subcategory_id": p.subcategory_id,
            "category_name": category_name,
            "subcategory_name": subcategory_name,
            "images": images
        })
    return jsonify({"products": products_list})

@main.route('/api/projects')
def api_projects():
    projects = Project.query.all()
    projects_list = []
    for pr in projects:
        images = [{"url": img.url, "alt_text": img.alt_text, "is_main": img.is_main} for img in pr.images]
        projects_list.append({
            "id": pr.id,
            "name": pr.name,
            "description": pr.description,
            "images": images
        })
    return jsonify({"projects": projects_list})

@main.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get(product_id)
    if not product:
        return "Sản phẩm không tồn tại", 404
    
    # # Lấy sp liên quan (cùng category, khác id)
    # related_products = Product.query.filter(
    #     Product.category_id == product.category_id,
    #     Product.id != product.id
    # ).limit(4).all()   # lấy 4 sp liên quan
    
    return render_template('product_detail.html', product=product)#, related_products=related_products)


@main.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get(project_id)
    if not project:
        return "Công trình không tồn tại", 404

    return render_template('project_detail.html', project=project)  # , related_products=related_products)
