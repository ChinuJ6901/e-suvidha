from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import snowflake.connector

provider_bp = Blueprint("provider", __name__, url_prefix="/provider")


def get_snowflake_connection():
    return snowflake.connector.connect(
        user="DIVPREM",
        password="1Divprem@password",
        account="NMWYQZO-HI27180",
        warehouse="COMPUTE_WH",
        database="ESUVIDHA",
        schema="APPDATA"
    )


# ✅ Route: Station Dashboard (Only for Stations)
@provider_bp.route("/dashboard", methods=["GET"])
def provider_dashboard():
    if "user_id" not in session or session.get("user_type") != "STATION":
        flash("Unauthorized access!", "error")
        return redirect(url_for("main.login"))

    station_name = session.get("username")  # The station's name is stored as username

    print("🔥 SESSION DATA:", session)
    print("🚀 Fetching requests for:", station_name)  # Debugging

    conn = get_snowflake_connection()
    cur = conn.cursor()

    sql_query = """
        SELECT REQUEST_ID, USERNAME, MOBILE, SERVICE_TYPE, CURRENT_LOCATION, REQUEST_TIME
        FROM ESUVIDHA.APPDATA.CHARGING_REQUESTS
        WHERE UPPER(STATION_NAME) = UPPER(%s) AND STATUS = 'open'
        ORDER BY REQUEST_TIME DESC;
    """

    cur.execute(sql_query, (station_name,))
    rows = cur.fetchall()

    # Convert results into a dictionary for easier use in Jinja
    requests = [
        {
            "REQUEST_ID": row[0],
            "USERNAME": row[1],
            "MOBILE": row[2],
            "SERVICE_TYPE": row[3],
            "CURRENT_LOCATION": row[4],
            "REQUEST_TIME": row[5]
        }
        for row in rows
    ]

    print("✅ Fetched Requests:", requests)  # Debugging

    cur.close()
    conn.close()

    return render_template("provider_dashboard.html", station_name=station_name, requests=requests)


# ✅ Route: Accept / Reject Requests
@provider_bp.route("/update_request", methods=["POST"])
def update_request():
    if "user_id" not in session or session.get("user_type") != "STATION":
        flash("Unauthorized access!", "error")
        return redirect(url_for("main.login"))

    request_id = request.form.get("request_id")
    action = request.form.get("action")  # Either 'accepted' or 'rejected'

    if not request_id or action not in ["accepted", "rejected"]:
        flash("Invalid request!", "error")
        return redirect(url_for("provider.provider_dashboard"))

    conn = get_snowflake_connection()
    cur = conn.cursor()

    sql_query = "UPDATE CHARGING_REQUESTS SET STATUS = %s WHERE REQUEST_ID = %s"
    cur.execute(sql_query, (action, request_id))

    conn.commit()
    cur.close()
    conn.close()

    flash(f"✅ Request {request_id} marked as {action}!", "success")
    return redirect(url_for("provider.provider_dashboard"))
