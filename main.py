from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

app = Flask(__name__)
conn_str = "mysql://root:5676@localhost/test"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


@app.route('/')
def hello():
    return "Online Test Portal"


@app.route('/register', methods=['GET', 'POST'])
def create_accounts():
    if request.method == 'POST':
        conn.execute(text("INSERT INTO accounts VALUES(:id, :f_name, :l_name, :pass, :account_type)"), request.form)
        conn.commit()
        # return render_template("register.html")
    return render_template("register.html")


@app.route('/accounts', methods=['GET', 'POST'])
def show_accounts():
    if request.method == 'POST':
        test_value = request.form["account_type"]
        if test_value == "all":
            accounts = conn.execute(text("SELECT * FROM accounts")).all()
            return render_template("accounts.html", accounts=accounts)
        elif test_value == "teacher":
            accounts = conn.execute(text("SELECT * FROM accounts WHERE account_type = 'teacher'")).all()
            return render_template("accounts.html", accounts=accounts)
        elif test_value == "student":
            accounts = conn.execute(text("SELECT * FROM accounts WHERE account_type = 'student'")).all()
            return render_template("accounts.html", accounts=accounts)
    return render_template("accounts.html")


@app.route('/creates', methods=['GET', 'POST'])
def create_test():
    # if request.method == 'POST':
    #     conn.execute(text("INSERT INTO accounts VALUES(:id, :f_name, :l_name, :pass, :account_type)"), request.form)
    #     conn.commit()
    teachers = conn.execute(text("SELECT * FROM accounts WHERE account_type = 'teacher'")).all()
    return render_template("create_test.html", teachers=teachers)


if __name__ == '__main__':
    app.run(debug=True)
