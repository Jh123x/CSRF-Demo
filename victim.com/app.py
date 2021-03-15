from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus, unquote_plus, parse_qs
from flask import Flask, request, render_template, redirect


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/data.db"
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    money = db.Column(db.Integer, nullable=False, default=500)

    def get_username(self) -> str:
        """Get the username of the user"""
        return self.username

    def compare_password(self, password: str) -> bool:
        """Get the password of the user"""
        return self.password == password

    def get_amount(self) -> int:
        return self.money

    def __repr__(self) -> str:
        return f"<User {self.username}>"


def get_user(username) -> User:
    usr = User.query.filter_by(username=username).first()
    return usr


db.create_all()
usrs = [get_user("admin"), get_user("alice"), get_user("bob")]
for u in usrs:
    if u:
        db.session.delete(u)
db.session.commit()

# Load default db
admin = User(username="admin", password="helloworld", is_admin=True, money=1000)
alice = User(username="alice", password="helloworld", is_admin=True, money=100000)
bob = User(username="bob", password="helloworld", is_admin=True, money=100000)
db.session.add(admin)
db.session.add(alice)
db.session.add(bob)
db.session.commit()


def user_loader(user_id, password) -> User:
    user = get_user(user_id)
    if user is None or not user.compare_password(password):
        return None
    return user


def decode_url(data: str):
    d = parse_qs(request.get_data().decode())
    for key, value in d.items():
        if key == "amount":
            value[0] = int(value[0])
        d[key] = value[0]
    return d


@app.route("/")
def index(msg=None):
    """Index for page"""
    name = request.cookies.get("userID")
    # If the person is logged in
    if name:
        user = get_user(name)
        return render_template(
            "index.html",
            name=name,
            result=f"{msg if msg else f'Welcome {name}'}",
            balance=user.get_amount(),
        )
    return render_template("index.html", name=False, result=msg if msg else "")


@app.route("/login", methods=["POST"])
def login():
    data = decode_url(request.get_data().decode())
    username = data.get("username")
    password = data.get("password")
    print(username, password)
    if username is None or password is None:
        """Either Username or password is not found"""
        return index("Please do not leave username or password blank")
    usr = get_user(username)
    if usr is None:
        return index("Username not found")
    user = user_loader(username, password)
    if user is None:
        return index("Wrong Password")
    # Parse the data
    resp = redirect("/")
    resp.set_cookie("userID", username)
    return resp


@app.route("/xfer", methods=["POST"])
def transfer():
    """Logic for transferring $$"""
    data = decode_url(request.get_data().decode())
    otheruser = data.get("name", None)
    amount = data.get("amount", None)
    if not (otheruser and get_user(otheruser)):
        return index(f"Other user is not found")
    if not request.cookies.get("userID"):
        return index(f"Please login")
    curr_user = get_user(request.cookies.get("userID"))
    if amount is None or curr_user.get_amount() < amount:
        return index(f"Amount is invalid / You do not have enough money")

    user_data = get_user(otheruser)
    user_data.money += amount
    curr_user.money -= amount
    db.session.commit()
    return index("Successfully Transferred")


@app.route("/logout", methods=["GET"])
def logout():
    resp = redirect("/")
    resp.delete_cookie("userID")
    return resp


if __name__ == "__main__":
    app.run("")
