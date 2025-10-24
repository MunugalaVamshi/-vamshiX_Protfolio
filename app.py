from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"   # change this in production

# MySQL Database Config
db_config = {
    'host': 'localhost',
    'user': 'root',        # your mysql username
    'password': '11d41F@0031', # your mysql password
    'database': 'vamshix'
}
# Database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)


# ✅ Home Page
@app.route("/")
def home():
    return render_template("index.html")


# ✅ Sign Up
@app.route("/signup", methods=["POST"])
def signup():
    fullname = request.form["fullname"]
    email = request.form["email"]
    password = generate_password_hash(request.form["password"])

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO register (fullname, email, password) VALUES (%s, %s, %s)", 
                       (fullname, email, password))
        conn.commit()
        flash("Account created successfully! Please login.", "success")
    except Error as e:
        flash("Error: Email may already exist.", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("home"))


# ✅ Sign In
@app.route("/signin", methods=["POST"])
def signin():
    email = request.form["email"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM register WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and check_password_hash(user["password"], password):
        session["user_id"] = user["id"]
        session["user_name"] = user["fullname"]
        flash("Login successful!", "success")
    else:
        flash("Invalid email or password", "danger")

    return redirect(url_for("home"))


# ✅ Contact Form
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contact (name, email, message) VALUES (%s, %s, %s)", 
                   (name, email, message))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Message sent successfully!", "success")
    return redirect(url_for("home"))


# ✅ Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
