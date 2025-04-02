from flask import Blueprint, render_template, request, redirect, url_for
import xml.etree.ElementTree as ET

user_bp = Blueprint("user", __name__, url_prefix="/user")

DATA_FILE = "data.xml"

@user_bp.route("/dashboard", methods=["GET"])
def user_dashboard():
    # Load charging stations from the XML file
    tree = ET.parse(DATA_FILE)
    root = tree.getroot()
    stations = []
    for station in root.find("charging_stations"):
        lat_element = station.find("lat")
        lng_element = station.find("lng")

        # Check if latitude and longitude exist, else assign default values
        lat = lat_element.text if lat_element is not None else "0"
        lng = lng_element.text if lng_element is not None else "0"

        stations.append({
            "name": station.find("name").text,
            "map_link": station.find("map_link").text,
            "lat": lat,
            "lng": lng
        })

    return render_template("user_dashboard.html", stations=stations)
