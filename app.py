from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, User, Staff, Trekker, Role, Diff, UserStatus, TrekStatus, BookStatus
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trek.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   
app.config['SECRET_KEY'] = 'my_key'  
db.init_app(app)  # connects the SQLAlchemy object to your Flask application

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context(): 
    db.create_all() 
    admin_name = "admin"
    admin_pwd = "adm123"
    admin_email = "admin@gmail.com"
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        adm = User(username=admin_name, email=admin_email, password=admin_pwd, role=Role.admin)
        db.session.add(adm)
        db.session.commit()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/adminlogin', methods = ['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')
        admin = User.query.filter_by(email=email).first()
        if not admin:
            return render_template('admin_login.html', error="Wrong Admin credentials!")
        if pwd != admin.password:
            return render_template('admin_login.html', error="Incorrect Password!")
        login_user(admin)
        return render_template('admin_dashboard.html')
    return render_template('admin_login.html')

@app.route('/userregister', methods=['GET','POST'])
def userregister():
    if request.method == 'POST':
        uname = request.form.get('username')
        email = request.form.get('email')
        pwd = request.form.get('password')
        role = request.form.get('role')
        user_new = User(username=uname, email=email, password=pwd, role=role)
        db.session.add(user_new)
        db.session.commit()

        if role == "staff":
            staff_new = Staff(user_id=user_new.id)
            db.session.add(staff_new)
            db.session.commit()
            return redirect('/stafflogin')
        
        elif role == "trekker":
            trekker_new = Trekker(user_id=user_new.id)
            db.session.add(trekker_new)
            db.session.commit()
            return redirect('/userlogin')

    return render_template('user_register.html')

@app.route('/stafflogin', methods=['GET','POST'])
def stafflogin():
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')
        staff = User.query.filter_by(email=email, role=Role.staff).first()
        if not staff:
            return render_template('staff_login.html', error="Staff not found!")
        if staff.password != pwd:
            return render_template('staff_login.html', error="Incorrect Password!")
        login_user(staff)
        return render_template('staff_dashboard.html')
    return render_template('staff_login.html')

@app.route('/userlogin', methods=['GET','POST'])
def userlogin():
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')
        trekker = User.query.filter_by(email=email, role=Role.trekker).first()
        if not trekker:
            return render_template('user_login.html', error="User not found!")
        if pwd != trekker.password:
            return render_template('user_login.html', error="Incorrect Password!")
        login_user(trekker)
        return render_template('user_dashboard.html')
    return render_template('user_login.html')

if __name__ == '__main__':
    app.run(debug=True)