from flask import Flask

def create_app():
    app = Flask(__name__, static_folder='static')
    app.secret_key = 'haha'

    from . import login, logout, reg, adminDashboard1, customerDashboard, index
    # import the Blueprints
    app.register_blueprint(login.bp)
    app.register_blueprint(reg.bp)
    app.register_blueprint(logout.bp)
    app.register_blueprint(index.bp)
    app.register_blueprint(adminDashboard1.bp)
    app.register_blueprint(customerDashboard.bp)

    return app