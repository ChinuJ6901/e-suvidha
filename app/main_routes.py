from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import snowflake.connector

main_bp = Blueprint('main', __name__)

def get_snowflake_connection():
    return snowflake.connector.connect(
        user="DIVPREM",
        password="1Divprem@password",
        account="NMWYQZO-HI27180",
        warehouse="COMPUTE_WH",
        database="ESUVIDHA",
        schema="APPDATA"
    )

@main_bp.route('/')
def home():
    return redirect(url_for('main.login'))

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to Snowflake and verify credentials
        conn = get_snowflake_connection()
        cur = conn.cursor()

        sql_query = "SELECT USER_ID, PASSWORD_HASH, USER_TYPE FROM USERS WHERE USERNAME = %s"
        cur.execute(sql_query, (username,))
        user_row = cur.fetchone()

        cur.close()
        conn.close()

        if user_row:
            user_id, stored_password, user_type = user_row  # Direct password comparison

            if stored_password == password:
                session["user_id"] = user_id
                session["user_type"] = user_type
                session["username"] = username  # ✅ Store the username in session

                flash("✅ Login successful!", "success")

                # Redirect based on user type
                if user_type == "EV_USER":
                    return redirect(url_for("user.user_dashboard"))
                elif user_type == "STATION":
                    return redirect(url_for("provider.provider_dashboard"))
                elif user_type == "ADMIN":
                    return redirect(url_for("admin.admin_dashboard"))
            else:
                flash("❌ Invalid password!", "error")
        else:
            flash("❌ User not found!", "error")

    return render_template("login.html")
