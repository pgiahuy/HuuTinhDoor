from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import Product, ProductImage, Category, SubCategory, Project, ProjectImage
import cloudinary.uploader

from . import db
admin = Blueprint('admin', __name__, url_prefix='/admin')

ADMIN_USER = "admin"
ADMIN_PASS = "1"

@admin.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USER and password == ADMIN_PASS:
            session["is_admin"] = True
            # flash("Đăng nhập thành công!", "success")
            return redirect(url_for("admin.dashboard"))
        #else:
            #flash("Sai tài khoản hoặc mật khẩu!", "danger")
    
    return render_template("login.html")

@admin.route("/dashboard")
def dashboard():
    
    if not session.get("is_admin"):
        flash("Bạn cần đăng nhập trước!", "warning")
        return redirect(url_for("admin.login"))


    categories = Category.query.all()
    subcategories = SubCategory.query.all()
    products = Product.query.all()

    # Tạo dict mapping để truy xuất nhanh
    category_dict = {c.id: c.name for c in categories}
    subcategory_dict = {s.id: s.name for s in subcategories}

    # products là danh sách sản phẩm từ DB

    return render_template("admin.html",
                            products=products,
                            categories=categories,
                            subcategories=subcategories,
                            category_dict=category_dict,
                            subcategory_dict=subcategory_dict)

@admin.route("/logout")
def logout():
    session.pop("is_admin", None)
    # flash("Đã đăng xuất!", "info")
    return redirect(url_for("main.index"))


@admin.route("/add_product", methods=["GET", "POST"])
def add_product():
    if not session.get("is_admin"):
        flash("Bạn cần đăng nhập!", "warning")
        return redirect(url_for("admin.login"))
    

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        category_id = request.form.get("category_id")
        subcategory_id = request.form.get("subcategory_id")
        files = request.files.getlist("images")
        main_index = int(request.form.get("main_image_index", 0))

        if not name or not price or not category_id or not subcategory_id:
            flash("Tên, giá, danh mục và loại sản phẩm là bắt buộc!", "danger")
            return redirect(url_for("admin.add_product"))

        # Tạo Product mới
        product = Product(
            name=name,
            description=description,
            price=float(price),
            category_id=int(category_id),
            subcategory_id=int(subcategory_id)
        )
        db.session.add(product)
        db.session.commit()


        folder_path = f"HuuTinhDoor/products/{product.subcategory.name}"
        
        # Upload nhiều ảnh
        for idx, file in enumerate(files):
            if file and file.filename != "":
                result = cloudinary.uploader.upload(file, folder=folder_path)
                image = ProductImage(
                    product_id=product.id,
                    url=result['secure_url'],
                    public_id=result['public_id'],
                    is_main=(idx == main_index)
                )
                db.session.add(image)

        db.session.commit()
        flash("Thêm sản phẩm thành công!", "success")
        return redirect(url_for("admin.dashboard"))
    
   

    return render_template(
        "admin.html"
    )


@admin.route("/add_project", methods=["GET", "POST"])
def add_project():
    if not session.get("is_admin"):
        flash("Bạn cần đăng nhập!", "warning")
        return redirect(url_for("admin.login"))

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        files = request.files.getlist("images")
        main_index = int(request.form.get("main_image_index", 0))

        if not name:
            flash("Tên là bắt buộc!", "danger")
            return redirect(url_for("admin.add_project"))

        # Tạo Project mới
        project = Project(
            name=name,
            description=description,
        )
        db.session.add(project)
        db.session.commit()

        folder_path = f"HuuTinhDoor/projects"

        # Upload nhiều ảnh
        for idx, file in enumerate(files):
            if file and file.filename != "":
                result = cloudinary.uploader.upload(file, folder=folder_path)
                image = ProjectImage(
                    project_id=project.id,
                    url=result['secure_url'],
                    public_id=result['public_id'],
                    is_main=(idx == main_index)
                )
                db.session.add(image)

        db.session.commit()
        flash("Thêm công trình thành công!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template(
        "admin.html"
    )


@admin.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    if not session.get("is_admin"):
        flash("Bạn cần đăng nhập!", "warning")
        return redirect(url_for("admin.login"))

    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        product.name = request.form.get("name")
        product.price = float(request.form.get("price"))
        product.description = request.form.get("description")
        product.category_id = int(request.form.get("category_id")) if request.form.get("category_id") else None

        if "image" in request.files:
            file = request.files["image"]
            if file.filename != "":
                # Xóa ảnh cũ
                for img in product.images:
                    cloudinary.uploader.destroy(img.public_id)
                    db.session.delete(img)

                # Upload ảnh mới
                result = cloudinary.uploader.upload(file)
                image = ProductImage(
                    url=result['secure_url'],
                    public_id=result['public_id'],
                    is_main=bool(request.form.get("is_main")),
                    product_id=product.id
                )
                db.session.add(image)

        db.session.commit()
        flash("Cập nhật sản phẩm thành công!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("edit_product.html", product=product)

# --- DELETE PRODUCT ---
@admin.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    if not session.get("is_admin"):
        flash("Bạn cần đăng nhập!", "warning")
        return redirect(url_for("admin.login"))

    product = Product.query.get_or_404(product_id)

    for img in product.images:
        cloudinary.uploader.destroy(img.public_id)
        db.session.delete(img)

    db.session.delete(product)
    db.session.commit()
    flash("Xóa sản phẩm thành công!", "success")
    return redirect(url_for("admin.dashboard"))