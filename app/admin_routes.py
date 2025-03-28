from flask import Blueprint, render_template, request, redirect, flash
import xml.etree.ElementTree as ET

admin_bp = Blueprint('admin', __name__)
DATA_FILE = 'data.xml'

@admin_bp.route('/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    tree = ET.parse(DATA_FILE)
    root = tree.getroot()

    users = root.find('users')
    user_list = []
    for user in users.findall('user'):
        user_list.append({
            'username': user.find('username').text,
            'type': user.get('type')
        })

    if request.method == 'POST':
        action = request.form['action']
        username = request.form['username']
        if action == 'add':
            user_type = request.form['user_type']
            password = request.form['password']
            new_user = ET.SubElement(users, 'user', type=user_type)
            ET.SubElement(new_user, 'username').text = username
            ET.SubElement(new_user, 'password').text = password
            tree.write(DATA_FILE)
            flash(f'User {username} added successfully.', 'success')
        elif action == 'remove':
            for user in users.findall('user'):
                if user.find('username').text == username:
                    users.remove(user)
                    tree.write(DATA_FILE)
                    flash(f'User {username} removed successfully.', 'success')
        return redirect('/admin/dashboard')

    return render_template('admin_dashboard.html', users=user_list)
