from flask import Blueprint, render_template, request, flash
import xml.etree.ElementTree as ET

provider_bp = Blueprint('provider', __name__)
DATA_FILE = 'data.xml'

@provider_bp.route('/dashboard', methods=['GET'])
def provider_dashboard():
    tree = ET.parse(DATA_FILE)
    root = tree.getroot()

    requests = root.find('charging_requests')
    charging_requests = []
    for request in requests.findall('request'):
        charging_requests.append({
            'user': request.find('username').text,
            'map_link': request.find('location').text
        })

    return render_template('provider_dashboard.html', requests=charging_requests)
