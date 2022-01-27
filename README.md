This is an individual project of Software Engineering.

# Technologies
- Python
- HTML
- CSS
- PostgreSQL
- ReactJS

# Libraries
- flask
- os
- random
- find_dotenv, load_dotenv
- requests
- flask_sqlalchemy
- flask_login

# APIs
- Spotify artist API (for an artist and all artist)
- Spotify top track API
- Genius search API

# Heroku
http://spotifymusicdiscovery.herokuapp.com/login

# Clones the repository
- In Visual Studio Code, creating a new directory where clone the code.
- Go to the current directory
- In the terminal, type:
    - git clone git@github.com:DuyBinhLeHa/MusicDiscovery.git
    - git install Flask
    - git install python-dotenv
    - git install requests
    - sudo apt update
    - sudo apt install postgresql
    - pip install psycopg2-binary
    - pip install Flask-SQLAlchemy==2.1
    - npm install
    - pip install -r requirements.txt
- Set up enviroment .env file:
    - In Spotify:
        - Go to https://developer.spotify.com/dashboard/
        - Log In/Sign up your account
        - Click CREATE AN APP to create your app
        - Copy Client ID and Client Secret and paste to .env file
    - In Genius:
        - Go to https://genius.com/signup_or_login
        - Sign Up/Log In your account
        - Click NEW API Client to create your app
        - Copy CLIENT ACCESS TOKEN and paste to .env file
    - In the terminal of VSCode (set up environment variable DATABASE_URL):
        - heroku login -i
        - heroku create
        - heroku addons:create heroku-postgresql:hobby-dev -a {your-app-name}
        - heroku config
        - Look at DATABASE_URL='value-in-here'
        - Copy value-in-here and paste to .env file

# Run Application
1. Run command in terminal (in your project directory): `npm run build`. This will update anything related to your `App.js` file (so `public/index.html`, any CSS you're pulling in, etc).
2. Run command in terminal (in your project directory): `python3 app.py`
3. Preview web page in browser 'localhost:8080/' (or whichever port you're using)

# Deploy to Heroku
1. Create a Heroku app: `heroku create --buildpack heroku/python`
2. Add nodejs buildpack: `heroku buildpacks:add --index 1 heroku/nodejs`
3. Push to Heroku: `git push heroku main`
4. Setup variables environment: go to Settings tab at Heroku > Reveal Config Vars

# a. What are at least 3 technical issues you encountered with your project? How did you fix them?
- When entering artist_id, every time when i press enter, then the page automatically reloads. To fix this situation, I have set onClick={} on button.
- After entering a list of artist_id, when I hit the save button, my entire database was deleted. The reason is that when I use for loop for list, if artist_id is invalid in the beginning, i will return error message. As a result, the following values ​​are not considered. To fix it, I set the flag variable to be able to check the entire artist_id list.
- I don't know how to show messages from flask.flash so I used flask.jsonify instead.

# b. What part of the stack do you feel most comfortable with? What part are you least comfortable with?
- I feel most comfortable with ReactJS and Python because I understood how Python works through Milestone 1 and 2 projects as well as understood how ReactJS works through the lecture.
- I least comfortable with mocking and without mocking.