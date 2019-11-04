from flask import Flask, render_template, request, flash, redirect, url_for, make_response
import flask
from forms import RegistrationForm, LoginForm, PostForm
import content_management as cm
app = Flask(__name__)

app.config['SECRET_KEY'] = '7ceffb97e94d7941410b951963815212'

class User:
	def __init__(self, username, password):
		self.username = username
		self.password = password
class Post:
	def __init__(self, title, author, body):
		self.title = title
		self.author = author
		self.body = body

menu = cm.getMenu()
loggedin = False
username = 'Diego Gutierrez'

users = [
	User("David Kennedy-Yoon", "password")
]

flask.app.user = User("","")
flask.app.loggedin = False



flask.app.posts = [
	Post("About", "Diego Gutierrez", "What is Davidbook? Davidbook was inspired by my roommate creating a groupchat for all the Davids in the freshman class. The premise of the website a is barebones Facebook for the Davids. Use the following username and password to login. 'David Kennedy-Yoon','password'"),
]

def valid_login(username, password):
	for user in users:
		if user.username == username and user.password == password:
			return True
	flash('Wrong Username or Password', 'danger')
	return False
	# return True

def log_the_user_in(user):
	print('switch to the main page')
	flask.app.loggedin = True
	flask.app.user = user
	print(flask.app.user.username)
	response = make_response(redirect(url_for('main')))
	response.headers['username'] = flask.app.user.username
	response.headers['loggedin'] = flask.app.user.password
	flash("Logged in " + str(flask.app.user.username), 'success')
	return response

@app.route("/")
@app.route("/main", methods=['GET','POST'])
def main():
	if request.method == "POST":
		print("POST")
	else:
		return render_template('main.html', menu = menu, username = flask.app.user.username, loggedin = flask.app.loggedin, posts = flask.app.posts) 

@app.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if valid_login(form.username.data, form.password.data):
			return log_the_user_in(User(form.username.data, form.password.data))
		else:
			print("Wrong Username or Password")
	return render_template('login.html', title = "Login", form = form, loggedin = flask.app.loggedin)

@app.route('/post', methods=['GET','POST'])
def post():
	form = PostForm()
	if form.validate_on_submit():
		flask.app.posts.append(Post(form.title.data, flask.app.user.username, form.body.data))
		flash('Post Created', 'success')
		return make_response(redirect(url_for('main')))
	return render_template('post.html', title = "Post", form = form, loggedin = flask.app.loggedin)

if __name__ == "__main__":
	app.run(debug = True)