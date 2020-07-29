from flask import Flask, request, render_template , url_for, flash, redirect
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
        return render_template('formulario.html')


@app.route('/edit/<id>')
def edit_contact(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id= %s', (id))
    data=cur.fetchall()
    cur.close()
    return render_template('edit_c.html', contact=data[0])


@app.route('/Update/<id>', methods= ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur=mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET Fullname = %s,
                Phone = %s,
                Email = %s
            WHERE  id = %s    
            """,(fullname,phone,email, id))
        mysql.connection.commit()
        flash("Contacto actualizado")
        return redirect(url_for('form'))


@app.route('/delete/<string:id>')
def delete_contact(id):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id={0}'.format(id))
    mysql.connection.commit()
    flash('Contact eliminado')
    return redirect(url_for('form'))


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
