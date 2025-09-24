from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import Product,ProductImage
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

@admin.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("is_admin"):
        flash("Bạn cần đăng nhập trước!", "warning")
        return redirect(url_for("admin.login"))

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        category_id = request.form.get("category_id")
        file = request.files.get("image")  # file input name="image"
        is_main = request.form.get("is_main") == "on"

        if not name or not price:
            flash("Tên và giá sản phẩm là bắt buộc!", "danger")
            return redirect(url_for("admin.dashboard"))

        # 1. tap Product moi
        product = Product(
            name=name,
            description=description,
            price=float(price),
            category_id=int(category_id) if category_id else None
        )
        db.session.add(product)
        db.session.commit()

        # 2. Upload ảnh lên Cloudinary
        if file:
            upload_result = cloudinary.uploader.upload(file)
            image_url = upload_result.get("secure_url")

            # 3. Tạo ProductImage
            product_image = ProductImage(
                product_id=product.id,
                url=image_url,
                alt_text=name,
                is_main=is_main
            )
            db.session.add(product_image)
            db.session.commit()

        flash("Thêm sản phẩm thành công!", "success")
        return redirect(url_for("admin.dashboard"))

    products = Product.query.all()
    return render_template("admin.html", products=products)

@admin.route("/logout")
def logout():
    session.pop("is_admin", None)
    # flash("Đã đăng xuất!", "info")
    return redirect(url_for("main.index"))


@admin.route("/add_product", methods=["GET", "POST"])
def add_product():
    if not session.get("is_admin"):
        flash("Bạn cần đăng nhập trước!", "warning")
        return redirect(url_for("admin.login"))
    
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        category_id = request.form.get("category_id")

        if not name or not price:
            flash("Tên và giá sản phẩm là bắt buộc!", "danger")
            return redirect(url_for("admin.add_product"))

        # tạo Product mới
        product = Product(
            name=name,
            description=description,
            price=float(price),
            category_id=int(category_id) if category_id else None
        )
        db.session.add(product)
        db.session.commit()

        flash("Thêm sản phẩm thành công!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("add_product.html")