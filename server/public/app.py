from flask import Flask
from flask_cors import CORS
from blueprints.auth import auth
from blueprints.admin import admin
from blueprints.engineer import engineer
from blueprints.customer import customer

app = Flask(__name__)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(engineer, url_prefix='/engineer')
app.register_blueprint(customer, url_prefix='/customer')

CORS(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)