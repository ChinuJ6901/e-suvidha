import xml.etree.ElementTree as ET

XML_FILE = 'app/data.xml'

def get_data():
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    return root

def save_data(root):
    tree = ET.ElementTree(root)
    tree.write(XML_FILE)

def find_user(username, role):
    root = get_data()
    for elem in root.find(f"{role}s"):
        if elem.find('username').text == username:
            return elem
    return None

def add_provider(username, password, google_maps_link):
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    providers = root.find("providers")

    provider = ET.Element("provider")
    ET.SubElement(provider, "id").text = str(len(providers) + 1)
    ET.SubElement(provider, "username").text = username
    ET.SubElement(provider, "password").text = password
    ET.SubElement(provider, "google_maps_link").text = google_maps_link

    providers.append(provider)
    tree.write(XML_FILE)
