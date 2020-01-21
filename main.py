from flask import Flask, render_template, request
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Petrovich137@'
app.config['MYSQL_DATABASE_DB'] = 'WebMed'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_SOCKET'] = None
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

mysql.init_app(app)



@app.route('/')
def main():
    return render_template('main.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')
    cursor.execute("SELECT * FROM users WHERE email = %s and password = %s", (str(login), str(password)))
    data = cursor.fetchone()
    conn.commit()
    if login and password and data != None:
        return render_template('main.html', results=data)
    elif login and password:
        return render_template('login.html', status='Invalid login or password')
    else:
        return render_template('login.html')


@app.route('/reg', methods=['GET', 'POST'])
def registration():
    first_name = request.form.get('first name')
    last_name = request.form.get('last name')
    email = request.form.get('email')
    user = request.form.get('user')
    password = request.form.get('password')
    if first_name is not None:
        cursor.execute("INSERT INTO users(name, surname, email, user_status, password) VALUES (%s, %s, %s, %s, %s)",
                       (str(first_name), str(last_name), str(email), str(user), str(password)))
        cursor.execute("SELECT * FROM users WHERE email = %s and password = %s", (str(email), str(password)))
        data = cursor.fetchone()
        conn.commit()
        return render_template('main.html', results=data)
    else:
        return render_template('registration.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
