from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import snowflake.connector
import datetime
import uuid  # Added for UUID generation

user_bp = Blueprint("user", __name__, url_prefix="/user")


# Snowflake Connection Function
def get_snowflake_connection():
    return snowflake.connector.connect(
        user="DIVPREM",
        password="1Divprem@password",
        account="NMWYQZO-HI27180",
        warehouse="COMPUTE_WH",
        database="ESUVIDHA",
        schema="APPDATA"
    )


# Fetch station data from Snowflake
def get_stations_from_snowflake():
    conn = get_snowflake_connection()
    cur = conn.cursor()

    sql_query = """
        SELECT NAME, MAP_LINK, LAT, LNG, RATING, REGULAR_CHARGES, FAST_CHARGES FROM STATIONS
    """
    cur.execute(sql_query)
    rows = cur.fetchall()

    stations = [
        {
            "name": row[0],
            "map_link": row[1],
            "lat": row[2],
            "lng": row[3],
            "rating": row[4],
            "regular_charges": row[5],
            "fast_charges": row[6]
        }
        for row in rows
    ]

    cur.close()
    conn.close()
    return stations


# User Dashboard
@user_bp.route("/dashboard", methods=["GET"])
def user_dashboard():
    stations = get_stations_from_snowflake()
    return render_template("user_dashboard.html", stations=stations)


# Booking Form Page
@user_bp.route("/book-charging-service", methods=["GET"])
def book_charging_service():
    station_name = request.args.get("station", "Unknown Station")
    return render_template("requestform.html", station_name=station_name)


# Submit Charging Request
@user_bp.route("/submit_request", methods=["POST"])
def submit_request():
    username = request.form.get("username")
    mobile = request.form.get("mobile")
    current_location = request.form.get("current_location")
    lat = request.form.get("lat")
    lng = request.form.get("lng")
    service_type = request.form.get("service_type")
    station_name = request.form.get("station_name")
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate a UUID for the request ID
    request_id = str(uuid.uuid4())

    # Insert into Snowflake
    conn = get_snowflake_connection()
    cur = conn.cursor()

    sql_query = """
        INSERT INTO CHARGING_REQUESTS 
        (REQUEST_ID, USERNAME, MOBILE, CURRENT_LOCATION, LAT, LNG, SERVICE_TYPE, STATION_NAME, REQUEST_TIME, STATUS)
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'open')
    """

    cur.execute(sql_query, (request_id, username, mobile, current_location, lat, lng, service_type, station_name, request_time))

    conn.commit()
    cur.close()
    conn.close()

    flash("✅ Charging request submitted successfully!", "success")

    # Redirect user to the tracking page with the UUID
    return redirect(url_for("user.track_request", request_id=request_id))


# Track Request Page
@user_bp.route("/track-request", methods=["GET"])
def track_request():
    request_id = request.args.get("request_id")

    if not request_id:
        flash("Invalid request ID!", "error")
        return redirect(url_for("user.user_dashboard"))

    conn = get_snowflake_connection()
    cur = conn.cursor()

    sql_query = "SELECT STATUS FROM CHARGING_REQUESTS WHERE REQUEST_ID = %s"
    cur.execute(sql_query, (request_id,))
    status_row = cur.fetchone()

    cur.close()
    conn.close()

    if not status_row:
        flash("Request not found!", "error")
        return redirect(url_for("user.user_dashboard"))

    status = status_row[0]  # Get current status

    return render_template("track_request.html", request_id=request_id, status=status)
