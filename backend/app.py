from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

db.init_app(app)

# Import models AFTER db initialization
from models.user import User

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return {
        "status": "success",
        "message": "VendorBridge ERP Backend Running"
    }


app.register_blueprint(auth_bp, url_prefix="/api/auth")
if __name__ == "__main__":
    app.run(debug=True)


