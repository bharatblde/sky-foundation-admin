from flask import Flask
from config import Config
from extensions import db, bcrypt
from routes.auth_routes import auth_bp
from routes.opportunity_routes import opp_bp
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = False

CORS(app,
     supports_credentials=True,
     origins=["http://127.0.0.1:5500"])

db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(opp_bp)

# ✅ ADD ROUTE HERE
@app.route("/")
def home():
    return "Backend is running 🚀"

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)