from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(
    database="service_db",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get('login'):
            username = request.form.get("username")
            password = request.form.get("password")
            if username != "" and password != "":
                cursor.execute("SELECT * FROM users WHERE u_login=%s AND u_password=%s", (username, password))
                records = cursor.fetchall()
                if not records:
                    return render_template("login.html", nonePerson=True)
                return render_template("account.html", full_name=records[0][1], login=username, password=password)
            else:
                return render_template("login.html", emptyString=True)
        elif request.form.get('registration'):
            return redirect('/registration/')
    return render_template("login.html")


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if (not name) or (not login) or (not password):
            return render_template('registration.html', emptyString=True)
        cursor.execute("SELECT users.u_login FROM users WHERE u_login=%s", (login,))
        users = cursor.fetchall()
        if users:
            return render_template('registration.html', userExist=True)
        cursor.execute('INSERT INTO users (u_name, u_login, u_password) VALUES( %s, %s, %s)',
                       (name, login, password))
        conn.commit()
        return redirect('/login/')
    return render_template('registration.html')
