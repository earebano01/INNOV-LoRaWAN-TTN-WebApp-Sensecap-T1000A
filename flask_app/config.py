path_db = '/var/ttn_tracker/ttn_tracker_database.db' # Chemin de la base de données SQLite

refresh_period_seconds = 15 # Période de rafraîchissement en secondes

start_lat = 47.6211 # Latitude de départ
start_lon = -65.67496 # Longitude de départ

cluster = "nam1" # Cluster utilisé

application = "sensecap-lora-tracker" # Application utilisée
app_key = "NNSXS.TGFGSOEXIKJROJXVOWTDUUOVWQH76LKAKOPLICI.7VSE4Z6NTIHL5WQBASAB7MX7COYW6CNL66NCVRTH5674DR4ZIKWQ" # Clé d'application

devices = [ # Liste des appareils
    "eui-2cf7f1c054600134",
    "eui-2cf7f1c0546005ed",
    "eui-a8610a34363a9216",
    "eui-2cf7f1c0541003c3"
]

gateway_locations = [ # Emplacements des passerelles
    ('ccnb-ido-gw', 47.6211945, -65.67475),
    ('eui-647fdafffe01a2dc-3', 47.6516938, -65.67487)
]

bing_api_key = 'AvYvx0oLrNB_CUoKLJibjitGAD7bB4o8i1bJMsPJodKBW2FftQUNSjB-Kfp9aQ8y' # Clé API Bing Maps

def config_app(app):
    # Configuration de l'application Flask pour utiliser la base de données SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{db}'.format(db=path_db)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app
