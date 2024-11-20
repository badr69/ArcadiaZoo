from flask import Flask, render_template
from forms import *


app = Flask(__name__)
app.secret_key = "manou"


@app.route('/', methods=['GET', 'POST'])
def index():
    reviewform = ReviewForm()
    return render_template('index.html', form=reviewform)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contactform = ContactForm()
    return render_template('contact.html', form=contactform)


@app.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        if loginform.email.data == "bad@email.com" and loginform.password.data == "123":
            return render_template("auth/success.html")
        else:
            return render_template("auth/denied.html")
    return render_template('auth/login.html', form=loginform)

@app.route('/logout')
def logout():
    return render_template("auth/logout.html")

if __name__ == '__main__':
    app.run(debug=True)
