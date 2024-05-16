# import datetime                                                             # Importation du module pour la gestion des dates et heures
# import json                                                                 # Importation du module pour la manipulation de données JSON
# import logging                                                              # Importation du module pour la journalisation des événements
# import os                                                                   # Importation du module pour les opérations sur le système d'exploitation
# import requests                                                             # Importation du module pour les requêtes HTTP
# from apscheduler.schedulers.background import BackgroundScheduler           # Importation du planificateur d'arrière-plan
# from dateutil.parser import parser                                          # Importation du parseur de dates
# from flask import Flask, jsonify, render_template                           # Importation de la classe Flask pour la création d'une application Web, jsonify pour la génération de réponses JSON et render_template pour le rendu des modèles HTML
# from flask_sqlalchemy import SQLAlchemy                                     # Importation de SQLAlchemy pour la gestion des bases de données SQL
# from math import atan2, cos, radians, sin, sqrt                             # Importation de fonctions mathématiques
# from flask import jsonify

# from config import app_key, application, bing_api_key, cluster, config_app, devices, gateway_locations, path_db, refresh_period_seconds, start_lat, start_lon

# # Configuration du journal d'événements
# logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
# logger = logging.getLogger(__name__)

# # Configuration de l'application Flask
# app = config_app(Flask(__name__, template_folder="./templates"))
# db = SQLAlchemy(app)
# app.app_context().push()

# # Planification de la récupération des nouvelles données
# def schedule_get_new_data():
#     get_new_data()

# scheduler = BackgroundScheduler()
# job = scheduler.add_job(schedule_get_new_data, 'interval', days=1)
# scheduler.start()
    
# class Location(db.Model):
#     __tablename__ = "location"

#     id = db.Column(db.Integer, primary_key=True)
#     added_at = db.Column(db.DateTime, default=datetime.datetime.now)
#     gateway_id = db.Column(db.String(250))  
#     device_id = db.Column(db.String(250))
#     raw = db.Column(db.Text)
#     datetime = db.Column(db.String(250))
#     datetime_obj = db.Column(db.DateTime)
#     latitude = db.Column(db.String(250))
#     longitude = db.Column(db.String(250))
#     temperature = db.Column(db.Float)    
#     humidity = db.Column(db.Float)    
#     pressure = db.Column(db.Float)    
#     altitude = db.Column(db.Float)    
#     rssi = db.Column(db.Integer)       
#     snr = db.Column(db.Integer)        

#     def __repr__(self):
#         return '<ID %r>' % self.id

#     @property
#     def serialize(self):
#         """Return object data in easily serializeable format"""
#         return {
#             'gateway_id': self.gateway_id,    
#             'device_id': self.device_id,
#             'datetime': self.datetime,
#             'latitude': self.latitude,
#             'longitude': self.longitude,
#             'temperature': self.temperature,       
#             'humidity': self.humidity or 0,     
#             'pressure': self.pressure or 0,     
#             'altitude': self.altitude or 0,     
#             'rssi': self.rssi,                
#             'snr': self.snr                
#         }
    
# class LastAcquisition(db.Model):
#     __tablename__ = "last_data"

#     id = db.Column(db.Integer, primary_key=True)
#     last_datetime = db.Column(db.DateTime)
#     gateway_id = db.Column(db.String(250))  
#     device_id = db.Column(db.String(250))
#     latitude = db.Column(db.String(250))
#     longitude = db.Column(db.String(250))
#     temperature = db.Column(db.Float)    
#     humidity = db.Column(db.Float)    
#     pressure = db.Column(db.Float)    
#     altitude = db.Column(db.Float)    
#     rssi = db.Column(db.Integer)       
#     snr = db.Column(db.Integer)        

#     def __repr__(self):
#         return '<ID %r>' % self.id

#     @property
#     def serialize(self):
#         """Return object data in easily serializeable format"""
#         return {
#             'gateway_id': self.gateway_id,     
#             'device_id': self.device_id,
#             'datetime': self.last_datetime,
#             'latitude': self.latitude,
#             'longitude': self.longitude,
#             'temperature': self.temperature,
#             'humidity': self.humidity or 0,     
#             'pressure': self.pressure or 0,     
#             'altitude': self.altitude or 0,       
#             'rssi': self.rssi,                
#             'snr': self.snr                  
#         }

# # Création de la base de données si elle n'existe pas
# if not os.path.exists(path_db):
#     db.create_all()

# # Route pour la page principale affichant la carte
# @app.route('/carte')
# def main_page():
#     get_new_data()
#     return render_template('carte.html',
#                            bing_api_key=bing_api_key,
#                            devices=devices,
#                            gateway_locations=gateway_locations,
#                            location_data=Location.query.all(),
#                            refresh_period_seconds=refresh_period_seconds,
#                            start_lat=start_lat,
#                            start_lon=start_lon)

# # Route pour récupérer les données passées
# # @app.route('/past/<seconds>')
# # def get_past_data(seconds):
# #     seconds_since_last = seconds_from_last()
# #     if seconds_since_last is not None and seconds_since_last > 10:
# #         get_new_data()

# #     if seconds == '0':
# #         markers = Location.query.all()
# #     else:
# #         past_dt_object = datetime.datetime.now() - datetime.timedelta(seconds=int(seconds))
# #         markers = Location.query.filter(Location.added_at > past_dt_object).all()
# #     return jsonify([i.serialize for i in markers])

# @app.route('/past/<seconds>')
# def get_past_data(seconds):
#     seconds_since_last = seconds_from_last()
#     if seconds_since_last is not None and seconds_since_last > 10:
#         get_new_data()

#     try:
#         seconds = int(seconds)
#     except ValueError:
#         return jsonify({"error": "Invalid time format"}), 400

#     if seconds == 0:
#         markers = Location.query.all()
#     else:
#         past_dt_object = datetime.datetime.now() - datetime.timedelta(seconds=seconds)
#         markers = Location.query.filter(Location.added_at > past_dt_object).all()
        
#     return jsonify([i.serialize for i in markers])


# # Fonction pour récupérer de nouvelles données
# def get_new_data():
#     last_seconds = seconds_from_last()
#     if last_seconds is not None:  
#         past_seconds = int(last_seconds) + 1
#     else:
#         past_seconds = 604800  

#     for each_device in devices:
#         endpoint = f"https://{cluster}.cloud.thethings.network/api/v3/as/applications/{application}/devices/{each_device}/packages/storage/uplink_message?order=-received_at&field_mask=up.uplink_message.decoded_payload,up.uplink_message.rx_metadata&time={past_seconds}s"  # Corrected the time variable here
#         logger.info(endpoint)
#         key = 'Bearer {}'.format(app_key)
#         headers = {'Accept': 'text/event-stream', 'Authorization': key}
#         try:
#             response = requests.get(endpoint, headers=headers)
#             if response.status_code != 200:
#                 logger.info(response.reason)
#                 continue  

#             response_format = "{\"data\": [" + response.text.replace("\n\n", ",")[:-1] + "]}"
#             response_data = json.loads(response_format)
#             uplink_msgs = response_data.get("data", [])

#             for uplink_msg in uplink_msgs:
#                 result = uplink_msg.get("result", {})
#                 uplink_message = result.get("uplink_message", {})
#                 decoded_payload = uplink_message.get("decoded_payload", {})
#                 rx_metadata = result.get("uplink_message", {}).get("rx_metadata", [{}])[0] 

#                 received = result.get("received_at", "")
#                 messages = decoded_payload.get("messages", [{}])
#                 temp, lat, lon = None, None, None
                
#                 # Check if messages list exists and contains expected keys
#                 if isinstance(messages, list) and messages:
#                     for message in messages:
#                         if "Air Temperature" in message:
#                             temp = message["Air Temperature"]
#                         if "Longitude" in message:
#                             lon = message["Longitude"]
#                         if "Latitude" in message:
#                             lat = message["Latitude"]

#                 # Fallback to direct payload fields if the structure differs
#                 if lat is None or lon is None:
#                     lat = decoded_payload.get("latitude", "")
#                     lon = decoded_payload.get("longitude", "")
#                 if temp is None:
#                     temp = decoded_payload.get("temperature", "")
                
#                 hum = decoded_payload.get("humidity", "")
#                 psr = decoded_payload.get("pressure", "")
#                 alt = decoded_payload.get("altitude", "")
#                 rssi = rx_metadata.get("rssi", "")  
#                 snr = rx_metadata.get("snr", "")    
#                 device = result.get("end_device_ids", {}).get("device_id", "")
#                 gateway_id = rx_metadata.get("gateway_ids", {}).get("gateway_id", "")  
#                 rawpay = uplink_message.get("frm_payload", "")

#                 if (received and lat and lon and not Location.query.filter(Location.datetime == received).first() and
#                         -90 < float(lat) <= 90 and -180 <= float(lon) <= 180):
#                     logger.info("{}, {}".format(lat, lon))
#                     new_location = Location(
#                         gateway_id=gateway_id,  
#                         device_id=device,
#                         raw=rawpay,
#                         datetime_obj=parser().parse(received),
#                         datetime=received,
#                         added_at=datetime.datetime.now(),
#                         latitude=lat,
#                         longitude=lon,
#                         temperature=float(temp) if temp else None,
#                         humidity=float(hum) if hum else None,
#                         pressure=float(psr) if psr else None,
#                         altitude=float(alt) if alt else None,
#                         rssi=float(rssi) if rssi else None,
#                         snr=float(snr) if snr else None)
#                     db.session.add(new_location)
#                     db.session.commit()
#                     logger.info(new_location)

#         except Exception as e:
#             logger.error(f"Error processing response: {e}")

#     set_date_now()

# # Fonction pour définir la date actuelle
# def set_date_now():
#     date_last = LastAcquisition.query.first()
#     if not date_last:
#         new_last = LastAcquisition(last_datetime=datetime.datetime.now())
#         db.session.add(new_last)
#         db.session.commit()
#     else:
#         date_last.last_datetime = datetime.datetime.now()
#         db.session.commit()

# # Fonction pour calculer le nombre de secondes depuis la dernière acquisition
# def seconds_from_last():
#     date_last = LastAcquisition.query.first()
#     if date_last:
#         return (datetime.datetime.now() - date_last.last_datetime).total_seconds()

# # Fonction pour calculer la distance entre deux coordonnées géographiques
# def distance_coordinates(lat1, lon1, lat2, lon2):
#     # Rayon approximatif de la Terre en km
#     R = 6373.0

#     lat1 = radians(lat1)
#     lon1 = radians(lon1)
#     lat2 = radians(lat2)
#     lon2 = radians(lon2)

#     dlon = lon2 - lon1
#     dlat = lat2 - lat1

#     a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
#     c = 2 * atan2(sqrt(a), sqrt(1 - a))

#     distance = R * c

#     return distance  # km


# # Fonction pour générer les données de heatmap
# def generateHeatmapData(locations):
#     heatmapData = []
#     for location in locations:
#         lat = float(location.latitude)
#         lon = float(location.longitude)
#         rssi = location.rssi
#         if lat and lon and rssi is not None:
#             heatmapData.append([lat, lon, rssi])  # Ajouter lat, lon et rssi à heatmapData
#     return heatmapData

# # Route pour récupérer les données de heatmap
# @app.route('/heatmap_data')
# def heatmap_data():
#     locations = Location.query.all()
#     heatmap_data = generateHeatmapData(locations)
#     return jsonify(heatmap_data)

# # Point d'entrée de l'application
# if __name__ == '__main__':
#     db.create_all()
#     app.run(debug=True, host='0.0.0.0', port=8000)

import datetime  # Importing modules for date and time management
import json  # Importing modules for JSON data manipulation
import logging  # Importing modules for event logging
import os  # Importing modules for operating system operations
import requests  # Importing modules for HTTP requests
from apscheduler.schedulers.background import BackgroundScheduler  # Importing the background scheduler
from dateutil.parser import parse  # Correcting the import for date parser
from flask import Flask, jsonify, render_template  # Importing Flask for web app creation, jsonify for JSON responses, and render_template for HTML templates
from flask_sqlalchemy import SQLAlchemy  # Importing SQLAlchemy for database management
from math import atan2, cos, radians, sin, sqrt  # Importing mathematical functions

# Importing configuration variables
from config import app_key, application, bing_api_key, cluster, config_app, devices, gateway_locations, path_db, refresh_period_seconds, start_lat, start_lon

# Configuring event logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

# Configuring the Flask application
app = config_app(Flask(__name__, template_folder="./templates"))
db = SQLAlchemy(app)
app.app_context().push()

# Scheduling the retrieval of new data
def schedule_get_new_data():
    get_new_data()

scheduler = BackgroundScheduler()
job = scheduler.add_job(schedule_get_new_data, 'interval', days=1)
scheduler.start()

# Database model for Location
class Location(db.Model):
    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)
    added_at = db.Column(db.DateTime, default=datetime.datetime.now)
    gateway_id = db.Column(db.String(250))
    device_id = db.Column(db.String(250))
    raw = db.Column(db.Text)
    datetime = db.Column(db.String(250))
    datetime_obj = db.Column(db.DateTime)
    latitude = db.Column(db.String(250))
    longitude = db.Column(db.String(250))
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    pressure = db.Column(db.Float)
    altitude = db.Column(db.Float)
    rssi = db.Column(db.Integer)
    snr = db.Column(db.Integer)

    def __repr__(self):
        return '<ID %r>' % self.id

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'gateway_id': self.gateway_id,
            'device_id': self.device_id,
            'datetime': self.datetime,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'temperature': self.temperature,
            'humidity': self.humidity or 0,
            'pressure': self.pressure or 0,
            'altitude': self.altitude or 0,
            'rssi': self.rssi,
            'snr': self.snr
        }

# Database model for LastAcquisition
class LastAcquisition(db.Model):
    __tablename__ = "last_data"

    id = db.Column(db.Integer, primary_key=True)
    last_datetime = db.Column(db.DateTime)
    gateway_id = db.Column(db.String(250))
    device_id = db.Column(db.String(250))
    latitude = db.Column(db.String(250))
    longitude = db.Column(db.String(250))
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    pressure = db.Column(db.Float)
    altitude = db.Column(db.Float)
    rssi = db.Column(db.Integer)
    snr = db.Column(db.Integer)

    def __repr__(self):
        return '<ID %r>' % self.id

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'gateway_id': self.gateway_id,
            'device_id': self.device_id,
            'datetime': self.last_datetime,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'temperature': self.temperature,
            'humidity': self.humidity or 0,
            'pressure': self.pressure or 0,
            'altitude': self.altitude or 0,
            'rssi': self.rssi,
            'snr': self.snr
        }

# Create the database if it does not exist
if not os.path.exists(path_db):
    db.create_all()

# Route for the main page displaying the map
@app.route('/carte')
def main_page():
    get_new_data()
    return render_template('carte.html',
                           bing_api_key=bing_api_key,
                           devices=devices,
                           gateway_locations=gateway_locations,
                           location_data=Location.query.all(),
                           refresh_period_seconds=refresh_period_seconds,
                           start_lat=start_lat,
                           start_lon=start_lon)

# Route for retrieving past data
# @app.route('/past/<seconds>')
# def get_past_data(seconds):
#     seconds_since_last = seconds_from_last()
#     if seconds_since_last is not None and seconds_since_last > 10:
#         get_new_data()

#     try:
#         seconds = int(seconds)
#     except ValueError:
#         return jsonify({"error": "Invalid time format"}), 400

#     if seconds == 0:
#         markers = Location.query.all()
#     else:
#         past_dt_object = datetime.datetime.now() - datetime.timedelta(seconds=seconds)
#         markers = Location.query.filter(Location.datetime > past_dt_object).all()

        
#     return jsonify([i.serialize for i in markers])

@app.route('/past/<seconds>')
def get_past_data(seconds):
    seconds_since_last = seconds_from_last()
    if seconds_since_last is not None and seconds_since_last > 10:
        get_new_data()

    try:
        seconds = int(seconds)
    except ValueError:
        return jsonify({"error": "Invalid time format"}), 400

    if seconds == 0:
        markers = Location.query.all()
    else:
        past_dt_object = datetime.datetime.now() - datetime.timedelta(seconds=seconds)
        markers = Location.query.filter(Location.datetime_obj > past_dt_object).all()  # Corrected filter to use datetime_obj

    return jsonify([i.serialize for i in markers])


# Function to retrieve new data
def get_new_data():
    last_seconds = seconds_from_last()
    if last_seconds is not None:
        past_seconds = int(last_seconds) + 1
    else:
        past_seconds = 604800  # Default to 7 days

    for each_device in devices:
        endpoint = f"https://{cluster}.cloud.thethings.network/api/v3/as/applications/{application}/devices/{each_device}/packages/storage/uplink_message?order=-received_at&field_mask=up.uplink_message.decoded_payload,up.uplink_message.rx_metadata&time={past_seconds}s"
        logger.info(endpoint)
        key = 'Bearer {}'.format(app_key)
        headers = {'Accept': 'text/event-stream', 'Authorization': key}
        try:
            response = requests.get(endpoint, headers=headers)
            if response.status_code != 200:
                logger.info(response.reason)
                continue

            response_format = "{\"data\": [" + response.text.replace("\n\n", ",")[:-1] + "]}"
            response_data = json.loads(response_format)
            uplink_msgs = response_data.get("data", [])

            for uplink_msg in uplink_msgs:
                result = uplink_msg.get("result", {})
                uplink_message = result.get("uplink_message", {})
                decoded_payload = uplink_message.get("decoded_payload", {})
                rx_metadata = result.get("uplink_message", {}).get("rx_metadata", [{}])[0]

                received = result.get("received_at", "")
                messages = decoded_payload.get("messages", [{}])
                temp, lat, lon = None, None, None

                if isinstance(messages, list) and messages:
                    for message in messages:
                        if "Air Temperature" in message:
                            temp = message["Air Temperature"]
                        if "Longitude" in message:
                            lon = message["Longitude"]
                        if "Latitude" in message:
                            lat = message["Latitude"]

                if lat is None or lon is None:
                    lat = decoded_payload.get("latitude", "")
                    lon = decoded_payload.get("longitude", "")
                if temp is None:
                    temp = decoded_payload.get("temperature", "")

                hum = decoded_payload.get("humidity", "")
                psr = decoded_payload.get("pressure", "")
                alt = decoded_payload.get("altitude", "")
                rssi = rx_metadata.get("rssi", "")
                snr = rx_metadata.get("snr", "")
                device = result.get("end_device_ids", {}).get("device_id", "")
                gateway_id = rx_metadata.get("gateway_ids", {}).get("gateway_id", "")
                rawpay = uplink_message.get("frm_payload", "")

                if (received and lat and lon and not Location.query.filter(Location.datetime == received).first() and
                        -90 < float(lat) <= 90 and -180 <= float(lon) <= 180):
                    logger.info("{}, {}".format(lat, lon))
                    new_location = Location(
                        gateway_id=gateway_id,
                        device_id=device,
                        raw=rawpay,
                        datetime_obj=parse(received),
                        datetime=received,
                        added_at=datetime.datetime.now(),
                        latitude=lat,
                        longitude=lon,
                        temperature=float(temp) if temp else None,
                        humidity=float(hum) if hum else None,
                        pressure=float(psr) if psr else None,
                        altitude=float(alt) if alt else None,
                        rssi=float(rssi) if rssi else None,
                        snr=float(snr) if snr else None)
                    db.session.add(new_location)
                    db.session.commit()
                    logger.info(new_location)

        except Exception as e:
            logger.error(f"Error processing response: {e}")

    set_date_now()

# Function to set the current date
def set_date_now():
    date_last = LastAcquisition.query.first()
    if not date_last:
        new_last = LastAcquisition(last_datetime=datetime.datetime.now())
        db.session.add(new_last)
        db.session.commit()
    else:
        date_last.last_datetime = datetime.datetime.now()
        db.session.commit()

# Function to calculate the number of seconds since the last acquisition
def seconds_from_last():
    date_last = LastAcquisition.query.first()
    if date_last:
        return (datetime.datetime.now() - date_last.last_datetime).total_seconds()

# Function to calculate the distance between two geographical coordinates
def distance_coordinates(lat1, lon1, lat2, lon2):
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

# Function to generate heatmap data
def generateHeatmapData(locations):
    heatmapData = []
    for location in locations:
        lat = float(location.latitude)
        lon = float(location.longitude)
        rssi = location.rssi
        if lat and lon and rssi is not None:
            heatmapData.append([lat, lon, rssi])
    return heatmapData

# Route to retrieve heatmap data
@app.route('/heatmap_data')
def heatmap_data():
    locations = Location.query.all()
    heatmap_data = generateHeatmapData(locations)
    return jsonify(heatmap_data)

# Entry point of the application
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8000)
