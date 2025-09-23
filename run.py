from flask import Flask, render_template
from app.models import db

app = Flask(__name__,template_folder='app/templates',static_folder='app/static')

# Kết nối MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost/huutinhdoor"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
