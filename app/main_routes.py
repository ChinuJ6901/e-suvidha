from flask import Blueprint, render_template, request, redirect, url_for, flash
import xml.etree.ElementTree as ET

main_bp = Blueprint('main', __name__)
DATA_FILE = 'data.xml'

@main_bp.route('/')
def home():
    return redirect(url_for('main.login'))

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Parse XML data
        tree = ET.parse(DATA_FILE)
        root = tree.getroot()

        # Check credentials and user type
        for user in root.find('users').findall('user'):
            if user.find('username').text == username and user.find('password').text == password:
                user_type = user.get('type')
                if user_type == 'user':
                    return redirect(url_for('user.user_dashboard'))
                elif user_type == 'provider':
                    return redirect(url_for('provider.provider_dashboard'))
                elif user_type == 'admin':
                    return redirect(url_for('admin.admin_dashboard'))

        flash('Invalid username or password', 'error')
        return redirect(url_for('main.login'))

    return render_template('login.html')
