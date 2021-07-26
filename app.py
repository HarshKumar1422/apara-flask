from flask import Flask, render_template, request, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_mysqldb import MySQL
import yaml
# i have tried khush easiest method not worked (redirecting one)
# jose easier method didnt worked
# jose hard method will try
app = Flask(__name__)

# Configure a secret SECRET_KEY
# We will later learn much better ways to do this!!
app.config['SECRET_KEY'] = 'mysecretkey'

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


class InfoForm(FlaskForm):
    '''
    This general class gets a lot of form about puppies.
    Mainly a way to go through many of the WTForms Fields.
    '''
    breed = StringField('')
    submit = SubmitField()


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/vision")
def vision():
    return render_template("vision.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        address = userDetails['address']
        age = userDetails['age']
        messege = userDetails['messege']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO abc(name, email,address,age,messege) VALUES(%s, %s,%s,%s,%s)",
                    (name, email, address, age, messege))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('thankyou', name=name))
    return render_template("contact.html")


@app.route("/thankyou/<name>")
def thankyou(name):
    # name = request.args.get('name')  this mwthod works only for get request..
    #email = request.args.get('last')
    return render_template("thankyou.html", name=name)


if __name__ == '__main__':
    app.run(debug=True)
