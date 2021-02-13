from flask import Flask
from flask_cors import CORS

from controllers.blueprint import cti_blueprint

app = Flask("ThreatIntelligenceApi")
CORS(app)

app.register_blueprint(cti_blueprint)

app.run("0.0.0.0", 8080)
