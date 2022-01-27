# pylint: disable = E1101, C0413, W1508, R0903, W0603, E0401

"""
Provides all the functions such as creating a model to store data in the database,
sign up, sign in, sign out, saving favorite artists according to each user.
"""
import os
import json
import random
import flask

from flask_login import login_user, current_user, LoginManager, logout_user
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv, find_dotenv

from genius import get_lyrics_link
from spotify import get_access_token, get_song_data, check_artist_id

load_dotenv(find_dotenv())

app = flask.Flask(__name__, static_folder="./build/static")
# This tells our Flask app to look at the results of `npm build` instead of the
# actual files in /templates when we're looking for the index page file. This allows
# us to load React code into a webpage. Look up create-react-app for more reading on
# why this is necessary.
bp = flask.Blueprint("bp", __name__, template_folder="./build")
# Point SQLAlchemy to your Heroku database
db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b"I am a secret key!"  # don't defraud my app ok?


##### MODELS #####
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    """
    Initialize User model to store the registered user.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))

    def __repr__(self):
        return f"<User {self.username}>"

    def get_username(self):
        """
        Return username when the function is called.
        """
        return self.username


class Artist(db.Model):
    """
    Initialize Artist model to store the favorite artists based on each user.
    """

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"<Artist {self.artist_id}>"


db.create_all()


### ROUTES ###
@bp.route("/index")
def index():
    """
    If the database does not exist any artist_id, then display the page without any information.
    Otherwise, randomly select artist_id from database. Based on artist_id to get information
    like song_name, song_artist, song_image_url, preview_url, genius_url and
    display them on index page.
    """
    artists = Artist.query.filter_by(username=current_user.username).all()
    artist_ids = [a.artist_id for a in artists]
    has_artists_saved = len(artist_ids) > 0
    if has_artists_saved:
        artist_id = random.choice(artist_ids)

        # API calls
        access_token = get_access_token()
        (song_name, song_artist, song_image_url, preview_url) = get_song_data(
            artist_id, access_token
        )
        genius_url = get_lyrics_link(song_name)

    else:
        (song_name, song_artist, song_image_url, preview_url, genius_url) = (
            None,
            None,
            None,
            None,
            None,
        )
    artist_data = {
        "has_artists_saved": has_artists_saved,
        "song_name": song_name,
        "song_artist": song_artist,
        "song_image_url": song_image_url,
        "preview_url": preview_url,
        "genius_url": genius_url,
        "username": current_user.username,
    }
    data = json.dumps(artist_data)
    return flask.render_template(
        "index.html",
        data=data,
    )


app.register_blueprint(bp)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_name):
    """
    Load user given an id.
    """
    return User.query.get(user_name)


@app.route("/signout", methods=["POST"])
def logout():
    """
    Log out of the current account and return to the login page.
    """
    logout_user()
    return flask.redirect(flask.url_for("login"))


@app.route("/signup")
def signup():
    """
    Render a signup page.
    """
    return flask.render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    """
    Get username from input text, check if this username is registered or not.
    If registered, do not allow that username to be saved to the database.
    Otherwise, allow that username to be saved to the database.
    Finally, it will go to the login page.
    """
    username = flask.request.form.get("username")
    user = User.query.filter_by(username=username).first()
    if user:
        pass
    else:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    return flask.redirect(flask.url_for("login"))


@app.route("/login")
def login():
    """
    Render a login page.
    """
    return flask.render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    """
    Get username from input text, check if this username is registered or not.
    If registered, it will go to the index page. Otherwise, show error message.
    """
    username = flask.request.form.get("username")
    user = User.query.filter_by(username=username).first()
    if user:
        login_user(user)
        return flask.redirect(flask.url_for("bp.index"))
    return flask.jsonify({"status": 401, "reason": "Username or Password Error"})


@app.route("/")
def main():
    """
    If the user has logged in before, it will go to the index page.
    Otherwise, it will stay at the login page.
    """
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("bp.index"))
    return flask.redirect(flask.url_for("login"))


@app.route("/save", methods=["POST"])
def save():
    """
    Get artist_id from input text, check if this artist_id is valid or not.
    If invalid, it won't be saved to the database. Otherwise, check its existence in the database.
    If it already exists in the database, save it. Otherwise, don't save it.
    """
    artist_ids = flask.request.json.get("new_artist")
    print(artist_ids)
    artist_available = []
    db.session.query(Artist).delete()
    db.session.commit()
    flag = 0

    for item in artist_ids:
        access_token = get_access_token()
        check_artist = check_artist_id(item, access_token)
        if check_artist:
            artist_available.append(item)
            flag = 1

    if flag == 1:
        username = current_user.username
        for artist_val in artist_available:
            db.session.add(Artist(artist_id=artist_val, username=username))
            db.session.commit()
        return flask.jsonify({"status": 200, "reason": "Artist ID has been saved"})
    return flask.jsonify({"status": 401, "reason": "Invalid artist ID entered"})


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8081)), debug=True
    )
