from master.agent_interface import comms
from master.database.models import User
from master.database.database_manager import db
from passlib.hash import sha256_crypt

app = None

@comms.action("register", ["start"])
def register(handler, message):
    password_hash = sha256_crypt.hash(message["password"])
    user = User(username=message["username"],
                password=password_hash,
                email=message["email"],
                first_name=message["first_name"],
                last_name=message["last_name"],
                role=message["role"])
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        return {"role": "{}".format(user.role), "response": "yes"}

@comms.action("login", ["start"])
def register(handler, message):
    password_hash = sha256_crypt.hash(message["password"])
    # need to decrypt password and compare
    email = message["email"]
    with app.app_context():
        user = User.query.filter_by(email=email).first()
    return {"role": "{}".format(user.role), "response": "yes"}

def run_agent_server(master):
    global app
    app = master
    comms.run(12345)
