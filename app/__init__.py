import os
from flask import Flask 
from flask_hashing import Hashing
app = Flask(__name__)





app.secret_key = '43@@y*f5FI4cPx~'
app.config["SECRET_KEY"] = "43@@y*f5FI4cPx~"

app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static')
app.config.update(SESSION_COOKIE_SAMESITE = 'Lax', SESSION_COOKIE_SECURE=True)

if os.environ.get('PYTHONANYWHERE_SITE'):
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

hashing = Hashing(app)
PASSWORD_SALT = '42##Z*f6EH1dQx~'

# Import views so Flask can find them
from . import views
