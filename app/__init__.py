from flask import Flask
from flask_mysqldb import MySQL

from . import index

# from app import yourPyFileName
# from app import login,admin,logout
# from app import temporaryIndex

mysql = MySQL()

def create_app():
    app = Flask(__name__, static_folder='static')
    app.secret_key = 'group1-project2'

    # Configure mysql database
    app.config['MYSQL_HOST'] = '127.0.0.1'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'lincoln2023'
    app.config['MYSQL_DB'] = 'takeaway'
    app.config['MYSQL_PORT'] = 3306
    
    mysql.init_app(app) 

    from . import login, logout, reg, adminDashboard1, customerDashboard, index
    # import the Blueprints
    app.register_blueprint(login.bp)
    app.register_blueprint(reg.bp)
    app.register_blueprint(logout.bp)
    app.register_blueprint(index.bp)
    app.register_blueprint(adminDashboard1.bp)
    app.register_blueprint(customerDashboard.bp)

    return app