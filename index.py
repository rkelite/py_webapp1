from flask import Flask, request, render_template , url_for, flash
from flask_mysqldb import MySQL, MySQLdb

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'Carlos'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'contacts_test'
mysql = MySQL(app)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)", (fullname, phone, email))
        mysql.connection.commit()
        flash("Contacto agregado")
        return render_template("formulario.html")


@app.route('/edit')
def edit_contact():
    return "edit_contact"

@app.route('/delete_contact')
def delete_contact():
    return "delete_contact"

@app.route('/form')
def form():
    cur=mysql.connection.cursor()
    cur.execute('Select * from  contacts')
    data=cur.fetchall()
    return render_template('formulario.html',contacts=data)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__=='__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port=3000, debug=True)   
