from flask import Blueprint, render_template, request, redirect, flash
import xml.etree.ElementTree as ET

user_bp = Blueprint('user', __name__)
DATA_FILE = 'data.xml'

@user_bp.route('/dashboard', methods=['GET', 'POST'])
def user_dashboard():
    tree = ET.parse(DATA_FILE)
    root = tree.getroot()

    charging_stations = root.find('charging_stations')
    stations = []
    for station in charging_stations.findall('station'):
        stations.append({
            'name': station.find('name').text,
            'map_link': station.find('map_link').text
        })

    if request.method == 'POST':
        # Handle remote charging kit request
        selected_station = request.form['station']
        for station in charging_stations.findall('station'):
            if station.find('name').text == selected_station:
                station_location = station.find('map_link').text
                flash(f'Remote charging request sent to {selected_station}. They can view your location.', 'success')
                return redirect(station_location)

    return render_template('user_dashboard.html', stations=stations)
