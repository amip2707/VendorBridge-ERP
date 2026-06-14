from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from extensions import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
CORS(app)

from models.user import User
from models.vendor import Vendor

from routes.auth_routes import auth_bp
from routes.vendor_routes import vendor_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(vendor_bp, url_prefix="/api")

@app.route("/")
def home():
    return {
        "status": "success",
        "message": "VendorBridge ERP Backend Running"
    }

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)