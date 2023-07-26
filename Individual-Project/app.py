from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyAk-CGIrlKQIsA3dtvZqXCgFoNeRzSxFqU",
  "authDomain": "y2individual-sam.firebaseapp.com",
  "projectId": "y2individual-sam",
  "storageBucket": "y2individual-sam.appspot.com",
  "messagingSenderId": "927509153747",
  "appId": "1:927509153747:web:10a50289cf9bf0769e5126",
  "measurementId": "G-63TDNRKZ67",
  "databaseURL": "https://y2individual-sam-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            print("trying")
            login_session['user'] = auth.create_user_with_email_and_password(email,password)
            UID = login_session['user']['localId']
            user = {"username":request.form['username'],"bio":request.form['bio']}
            db.child("Users").child(UID).set(user)
            print("added")
            return redirect(url_for('discover'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")

@app.route('/discover')
def discover():
    error = ""
    try:
        n = db.child("Posts").get().val()
        print("posts value assigned successfully")
        return render_template("discover.html",posts = n)
    except:
        error = "Could not retrieve posts at this moment, please refresh and try again later."
        return render_template("discover.html", error=error)



@app.route('/signout')
def signout():
    login_session['user']= None
    auth.current_user = None
    return redirect(url_for('home'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('discover'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/profile')
def profile():
    UID = login_session["user"]["localId"]
    current_user = db.child("Users").child(UID).get().val()
    return render_template("profile.html", user = current_user)

@app.route('/post',methods=['GET','POST'])
def add_post():
    error=""
    if request.method == 'POST':
        title = request.form["title"]
        caption = request.form["caption"]
        UID = login_session["user"]["localId"]
        current_user = db.child("Users").child(UID).get().val()
        try:
            post = {"username":current_user["username"],"title":title,"caption":caption,"comments":[]}      # title, caption, [(UID, text),(Akjsd72HADus, "Hi! Great work!"),()]
            print("trying, created the post")
            db.child("Posts").push(post)
            print("added the post")
            return redirect(url_for('discover'))
        except:
            error="failed to post"
    return render_template("post.html")

@app.route('/add_comment', methods=['GET','POST'])
def add_comment():
    error=""
    if request.method == 'POST':
        comment = request.form["comment"]
        UID = login_session["user"]["localId"]

        postID = request.form["post_id"]

        comments_template = (UID, comment)#tuple
        try:
            db.child("Posts").child(postID).push(comments_template)
        except:
            print("sade")
    return redirect(url_for("discover.html"))

#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)

"""@app.route('/about')
def about():
    UID = login_session["user"]["localId"]
    print(f"UID: {UID}")
    current_user = db.child("Users").child(UID).get().val()
    return render_template("about.html", username = current_user)"""