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
                role="customer")
    with app.app_context():
        db.session.add(user)
        db.session.commit()
    return {}

def run_agent_server(master):
    global app
    app = master
    comms.run(12345)
