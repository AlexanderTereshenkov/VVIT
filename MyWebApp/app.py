from flask import Flask, render_template, request
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


@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username != "" and password != "":
        cursor.execute("SELECT * FROM users WHERE u_login=%s AND u_password=%s", (username, password))
        records = cursor.fetchall()
        if len(records) == 0:
            return render_template("account.html", nonePerson="")
        return render_template("account.html", full_name=records[0][1], login=username, password=password)
    return render_template("account.html", full_name="")


@app.get('/login/')
def index():
    return render_template('login.html')
